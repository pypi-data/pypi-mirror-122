# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from pathlib import Path as path_t
from typing import Callable, Optional, Sequence, Union

import numpy as nmpy
import scipy.optimize as spop
import skimage.morphology as mrph
import skimage.segmentation as sgmt
import tensorflow.keras.models as modl
import tqdm
from scipy import ndimage as image_t
from scipy.spatial import distance as dstc

from cell_tracking_BC.task.jaccard import PseudoJaccard


array_t = nmpy.ndarray
processing_h = Callable[[array_t], array_t]


def SegmentationsWithTFNetwork(
    frames: Sequence[array_t],
    network_path: Union[str, path_t],
    /,
    *,
    threshold: float = 0.9,
    PreProcessed: processing_h = None,
    PostProcessed: processing_h = None,
) -> Sequence[array_t]:
    """
    PostProcessed: Could be used to clear border objects. However, since one might want to segment cytoplasms and
    nuclei, clearing border objects here could lead to clearing a cytoplasm while keeping its nucleus. Consequently,
    clearing border objects here, i.e. independently for each segmentation task, is not appropriate. Instead, it has
    been deferred to frame_t.AddCellsFromSegmentations.
    """
    output = []

    if PreProcessed is not None:
        frames = tuple(PreProcessed(_frm) for _frm in frames)
    if PostProcessed is None:
        PostProcessed = lambda _prm: _prm

    frames = nmpy.array(frames, dtype=nmpy.float32)
    if frames.ndim == 3:
        frames = nmpy.expand_dims(frames, axis=3)

    network = modl.load_model(network_path)
    predictions = network.predict(frames, verbose=1)
    shape = network.layers[0].input_shape[0][1:-1]

    for t_idx, prediction in enumerate(predictions):
        reshaped = nmpy.reshape(prediction, shape)
        segmentation = reshaped > threshold
        post_processed = PostProcessed(segmentation)
        if nmpy.amax(post_processed.astype(nmpy.uint8)) == 0:
            raise ValueError(f"{t_idx}: Empty segmentation")

        output.append(post_processed)

    return output


def CorrectSegmentationBasedOnTemporalCoherence(
    segmentation: array_t,
    previous: array_t,
    /,
    *,
    min_jaccard: float = 0.75,
    max_area_discrepancy: float = 0.25,
) -> Optional[array_t]:
    """
    Actually, Pseudo-Jaccard
    """
    original = None

    labeled, n_cells = mrph.label(segmentation, return_num=True, connectivity=1)
    labeled_previous, n_cells_previous = mrph.label(
        previous, return_num=True, connectivity=1
    )

    cells_idc = nmpy.fromiter(range(1, n_cells + 1), dtype=nmpy.uint64)
    cells_idc_previous = nmpy.fromiter(
        range(1, n_cells_previous + 1), dtype=nmpy.uint64
    )
    # Note the reversed parameter order in PseudoJaccard since a fusion is a division in reversed time
    _PseudoJaccard = lambda idx_1, idx_2: PseudoJaccard(
        labeled, labeled_previous, idx_2, idx_1
    )
    pairwise_jaccards = dstc.cdist(
        cells_idc_previous[:, None], cells_idc[:, None], metric=_PseudoJaccard
    )

    tp1_to_t_associations = {}
    while True:
        row_ind, col_ind = spop.linear_sum_assignment(1.0 - pairwise_jaccards)
        valid_idc = pairwise_jaccards[row_ind, col_ind] > min_jaccard
        if not nmpy.any(valid_idc):
            break
        for key, value in zip(col_ind[valid_idc], row_ind[valid_idc]):
            if key in tp1_to_t_associations:
                tp1_to_t_associations[key].append(value)
            else:
                tp1_to_t_associations[key] = [value]
        pairwise_jaccards[row_ind, :] = 0.0

    for label in range(1, n_cells + 1):
        previous_labels = tp1_to_t_associations.get(label - 1)
        if (previous_labels is not None) and (previous_labels.__len__() > 1):
            previous_labels = nmpy.array(previous_labels)
            previous_labels += 1

            where_fused = labeled == label
            fused_area = nmpy.count_nonzero(where_fused)

            seeds = nmpy.zeros_like(labeled_previous)
            for l_idx, previous_label in enumerate(previous_labels, start=1):
                seeds[labeled_previous == previous_label] = l_idx
            seeds_area = nmpy.count_nonzero(seeds)
            if (
                discrepancy := abs(seeds_area - fused_area) / fused_area
            ) > max_area_discrepancy:
                print(
                    f"/!\\ Segmentation correction discarded due to high t-total-area/(t+1)-fused-area discrepancy "
                    f"({discrepancy}) between cells {previous_labels} and fused cell {label}"
                )
                continue

            seeds[nmpy.logical_not(where_fused)] = 0
            # Just in case zeroing the non-fused region deleted some labels. If this can happen, it must be in very
            # pathological cases.
            seeds, *_ = sgmt.relabel_sequential(seeds)
            if (n_seeds := nmpy.amax(seeds)) != previous_labels.size:
                # Should never happen (see comment above)
                print(
                    f"/!\\ Segmentation correction discarded due to invalid watershed seeds: "
                    f"Actual={n_seeds}; Expected={previous_labels.size}"
                )
                continue

            distance_map = image_t.distance_transform_edt(where_fused)
            separated = sgmt.watershed(
                -distance_map, seeds, mask=where_fused, watershed_line=True
            )

            original = segmentation.copy()
            segmentation[where_fused] = 0
            segmentation[separated > 0] = 1

    return original


def CorrectSegmentationsBasedOnTemporalCoherence(
    segmentations: Sequence[array_t], /, *, min_jaccard: float = 0.75
) -> Sequence[Optional[array_t]]:
    """
    Actually, Pseudo-Jaccard
    """
    originals = []

    for f_idx in tqdm.trange(
        1, segmentations.__len__(), desc="Segmentation Correction"
    ):
        original = CorrectSegmentationBasedOnTemporalCoherence(
            segmentations[f_idx], segmentations[f_idx - 1], min_jaccard=min_jaccard
        )
        originals.append(original)

    return originals
