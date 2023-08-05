"""Position related functions."""

import numpy as np

###################################################################################################
###################################################################################################

def compute_distance(x1, y1, x2, y2):
    """Compute the distance between two positions.

    Parameters
    ----------
    x1, y1 : float
        The X & Y values for the first position.
    x2, y2 : float
        The X & Y values for the second position.

    Returns
    -------
    float
        Distance between the two positions.

    Examples
    --------
    Compute distance between the two points (x1, y1) and (x2, y2):

    >>> x1, x2 = 1, 5
    >>> y1, y2 = 6, 9
    >>> compute_distance(x1, y1, x2, y2)
    5.0
    """

    return np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))


def compute_distances(xs, ys):
    """Compute distances across a sequence of positions.

    Parameters
    ----------
    xs, ys : 1d array
        Position data, of X and Y locations.

    Returns
    -------
    1d array
        Vector of distances between positions.

    Examples
    --------
    Compute distances between vectors of x- and y-positions:

    >>> xs, ys = np.array([1, 2, 3, 4, 5]), np.array([6, 7, 8, 9, 10])
    >>> compute_distances(xs, ys)
    array([1.41421356, 1.41421356, 1.41421356, 1.41421356])
    """

    dists = np.zeros(len(xs) - 1)
    for ix, (xi, yi, xj, yj) in enumerate(zip(xs, ys, xs[1:], ys[1:])):
        dists[ix] = compute_distance(xi, yi, xj, yj)

    return dists


def compute_cumulative_distances(xs, ys):
    """Compute cumulative distance across a sequence of positions.

    Parameters
    ----------
    xs, ys : 1d array
        Position data, of X and Y locations.

    Returns
    -------
    1d array
        Cumulative distances.

    Examples
    --------
    Compute cumulative distances between vectors of x- and y-positions:

    >>> xs, ys = np.array([1, 2, 3, 4, 5]), np.array([6, 7, 8, 9, 10])
    >>> compute_cumulative_distances(xs, ys)
    array([1.41421356, 2.82842712, 4.24264069, 5.65685425])
    """

    return np.cumsum(compute_distances(xs, ys))


def compute_speed(xs, ys, bin_widths):
    """Compute speeds across a sequence of positions.

    Parameters
    ----------
    xs, ys : 1d array
        Position data, of X and Y locations.
    bin_widths : 1d array
        Width of each position bin.

    Returns
    -------
    speed : 1d array
        Vector of speeds across each position step.

    Examples
    --------
    Compute speed across vectors of x- and y-positions:

    >>> xs, ys = np.array([1, 2, 3, 4, 5]), np.array([6, 7, 8, 9, 10])
    >>> bin_width = np.array([1, 1, 0.5, 1])
    >>> compute_speed(xs, ys, bin_width)
    array([1.41421356, 1.41421356, 2.82842712, 1.41421356])
    """

    distances = compute_distances(xs, ys)
    speed = distances / bin_widths

    return speed
