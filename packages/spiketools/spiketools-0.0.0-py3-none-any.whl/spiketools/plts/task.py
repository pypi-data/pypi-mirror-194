"""Plots for tasks and task structure related visualizations."""

import matplotlib.pyplot as plt

from spiketools.plts.annotate import add_vshades, add_vlines
from spiketools.plts.utils import check_ax, savefig
from spiketools.plts.style import set_plt_kwargs

###################################################################################################
###################################################################################################

@savefig
@set_plt_kwargs
def plot_task_structure(task_ranges=None, event_lines=None, data_points=None,
                        range_colors=None, line_colors=None, range_kwargs=None, event_kwargs=None,
                        ax=None, **plt_kwargs):
    """Plot task structure, shaded ranges of event durations, and lines of point events.

    Parameters
    ----------
    task_ranges : list of list of float, optional
        List of start and end ranges to shade in, to indicate event durations.
        To add multiple different shaded regions, pass a list of multiple shade definitions.
    event_lines : list of float, optional
        Timestamps at which to draw vertical lines, to indicate point events.
        To add multiple different lines, pass a list of multiple line definitions.
    data_points : 1d array, optional
        Set of timestamps to indicate data points of interest on the plot.
    range_colors : list of str, optional
        Colors to plot the ranges in. Used if passing multiple task range sections.
    line_colors : list of str, optional
        Colors to plot the lines in. Used if passing multiple line sections.
    range_kwargs : dict, optional
        Additional keyword arguments for the range shades.
    event_kwargs : dict, optional
        Additional keyword arguments for the event lines.
    ax : Axes, optional
        Axis object upon which to plot.
    plt_kwargs
        Additional arguments to pass into the plot function.
    """

    ax = check_ax(ax, figsize=plt_kwargs.pop('figsize', (16, 2)))

    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    range_kwargs = {} if range_kwargs is None else range_kwargs
    event_kwargs = {} if event_kwargs is None else event_kwargs

    if task_ranges is not None:
        if not isinstance(task_ranges[0][0], (int, float)):
            for trange, color in zip(task_ranges, range_colors if range_colors else color_cycle):
                range_kwargs['color'] = color
                plot_task_structure(task_ranges=trange, range_kwargs=range_kwargs, ax=ax)
        else:
            range_kwargs.setdefault('alpha', 0.25)
            shade_ranges = [[st, en] for st, en in zip(*task_ranges)]
            add_vshades(shade_ranges, **range_kwargs, ax=ax)

    if event_lines is not None:
        if not isinstance(event_lines[0], (int, float)):
            for eline, color in zip(event_lines, line_colors if line_colors else color_cycle):
                event_kwargs['color'] = color
                plot_task_structure(event_lines=eline, event_kwargs=event_kwargs, ax=ax)
        else:
            add_vlines(event_lines, **event_kwargs, ax=ax)

    if data_points is not None:
        ax.eventplot(data_points)

    plt.yticks([])
