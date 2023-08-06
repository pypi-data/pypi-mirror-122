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

import matplotlib.pyplot as pypl
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t

from cell_tracking_BC.in_out.graphics.generic import FinalizeDisplay
from cell_tracking_BC.in_out.file.archiver import archiver_t
from cell_tracking_BC.type.sequence import sequence_t
from cell_tracking_BC.type.track import single_track_t


def ShowTracking(
    sequence: sequence_t,
    /,
    *,
    with_track_labels: bool = True,
    with_cell_labels: bool = True,
    show_and_wait: bool = True,
    figure_name: str = "segmentation",
    archiver: archiver_t = None,
) -> None:
    """"""
    figure = pypl.figure()
    axes = figure.add_subplot(projection=axes_3d_t.name)
    axes.set_xlabel("row positions")
    axes.set_ylabel("column positions")
    axes.set_zlabel("time points")

    colors = "bgrcmyk"
    max_time_point = 0
    for t_idx, track in enumerate(sequence.tracks):
        color_idx = t_idx % colors.__len__()

        if isinstance(track, single_track_t):
            branches = (track,)
        else:
            branches = track.Branches()
        for branch in branches:
            rows, cols, times, *labels = branch.AsRowsColsTimes(
                with_labels=with_cell_labels
            )
            if times[-1] > max_time_point:
                max_time_point = times[-1]

            axes.plot3D(rows, cols, times, colors[color_idx])

            if with_cell_labels:
                for row, col, time, label in zip(rows, cols, times, labels[0]):
                    axes.text(
                        row,
                        col,
                        time,
                        str(label),
                        fontsize="x-small",
                        color=colors[color_idx],
                    )
            if with_track_labels and (branch.label is not None):
                axes.text(
                    rows[-1],
                    cols[-1],
                    times[-1] + 0.25,
                    str(branch.label),
                    fontsize="x-small",
                    color=colors[color_idx],
                    bbox={
                        "facecolor": "none",
                        "edgecolor": colors[color_idx],
                        "boxstyle": "round",
                    },
                )

    FinalizeDisplay(figure, figure_name, show_and_wait, archiver)
