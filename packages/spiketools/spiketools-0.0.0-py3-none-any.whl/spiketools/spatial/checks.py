"""Checker functions for spatial related functionality."""

###################################################################################################
###################################################################################################

def check_position(position):
    """Check a position array.

    Parameters
    ----------
    position : 1d or 2d array
        Position values.

    Raises
    ------
    AssertionError
        Raised if there are any issues with the given position array.
    """

    assert position.ndim in (1, 2), 'Position input should be 1d or 2d.'


def check_spatial_bins(bins, position=None):
    """Check a bin definition for binning spatial data.

    Parameters
    ----------
    bins : int or list of [int, int]
        The bin definition for dividing up the space. If 1d, can be integer.
        If 2d should be a list, defined as [number of x_bins, number of y_bins].
    position : 1d or 2d array, optional
        Position values across a 1d or 2d space.
        If provided, used to check consistency between position dimensionality and bin definition.

    Returns
    -------
    bins : list of [int] or list of [int, int]
        Bin definition, after checking, and converted to being a list.

    Raises
    ------
    AssertionError
        Raised if there are any issues with the given bin definition.
    """

    if isinstance(bins, int):
        bins = [bins]

    if isinstance(bins, list):
        for binval in bins:
            assert isinstance(binval, int), 'Bin definition values should be integers.'

    assert len(bins) <= 2, 'Bin definition has too many values (>2).'

    if position is not None:
        check_position(position)
        assert len(bins) == position.ndim, \
            'There is a mismatch between position data and bin definition.'

    return bins
