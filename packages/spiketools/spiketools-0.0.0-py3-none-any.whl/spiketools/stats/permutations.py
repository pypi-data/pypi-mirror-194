"""Permutation related functions."""

import numpy as np
from scipy.stats import zmap

from spiketools.plts.stats import plot_surrogates

###################################################################################################
###################################################################################################

def permute_vector(data, n_permutations=1000):
    """Create permutations of a vector of data.

    Parameters
    ----------
    data : 1d array
        Vector to permute.
    n_permutations : int, optional, default: 1000
        Number of permutations to do.

    Returns
    -------
    permutations : 2d array
        Permutations of the input data.

    Notes
    -----
    Code adapted from here: https://stackoverflow.com/questions/46859304/

    This function doesn't have any randomness - for a given array it will
    iterate through the same set of permutations, in sequence.

    Examples
    --------
    Create permutations for a vector of data:

    >>> data = np.array([0, 5, 10, 15, 20])
    >>> permute_vector(data, n_permutations=4)
    array([[ 0,  5, 10, 15, 20],
           [ 5, 10, 15, 20,  0],
           [10, 15, 20,  0,  5],
           [15, 20,  0,  5, 10]])
    """

    assert data.ndim == 1, 'The permute_vector function only works on 1d arrays.'

    data_ext = np.concatenate((data, data[:-1]))
    strides = data.strides[0]
    permutations = np.lib.stride_tricks.as_strided(data_ext,
                                                   shape=(n_permutations, len(data)),
                                                   strides=(strides, strides),
                                                   writeable=False).copy()

    return permutations


def compute_surrogate_pvalue(value, surrogates):
    """Compute the empirical p-value from a distribution of surrogates.

    Parameters
    ----------
    value : float
        Test value.
    surrogates : 1d array
        Distribution of surrogates.

    Returns
    -------
    float
        The empirical p-value.

    Examples
    --------
    Compute empirical p-value for a computed value compared to a distribution of surrogates:

    >>> value = 0.9
    >>> surrogates = np.random.normal(size=100)
    >>> pval = compute_surrogate_pvalue(value, surrogates)
    """

    return sum(surrogates > value) / len(surrogates)


def compute_surrogate_zscore(value, surrogates):
    """Compute the z-score of a real data value compared to a distribution of surrogates.

    Parameters
    ----------
    value : float
        Value to z-score.
    surrogates : 1d array
        Distribution of surrogates to compute the z-score against.

    Returns
    -------
    float
        The z-score of the given value.

    Examples
    --------
    Compute z-score for a computed value compared to a distribution of surrogates:

    >>> value = 0.9
    >>> surrogates = np.random.normal(size=100)
    >>> zscore = compute_surrogate_zscore(value, surrogates)
    """

    return zmap(value, surrogates)[0]


def compute_surrogate_stats(data_value, surrogates, plot=False, verbose=False, **plt_kwargs):
    """Compute surrogate statistics.

    Parameters
    ----------
    data_value : float
        Test value.
    surrogates : 1d array
        Distribution of surrogates values.
    plot : bool, optional, default: False
        Whether to display the plot of the surrogates values.
    verbose : bool, optional, default: False
        Whether to print the values of the p-value and z-score.

    Returns
    -------
    p_val : float
        The empirical p-value of the test value, as compared to the surrogates.
    z_score : float
        The z-score of the test value, as compared to the surrogates.

    Examples
    --------
    Compute measures for a computed value compared to a distribution of surrogates:

    >>> value = 0.9
    >>> surrogates = np.random.normal(size=100)
    >>> p_val, z_score = compute_surrogate_stats(value, surrogates)
    """

    p_val = compute_surrogate_pvalue(data_value, surrogates)
    z_score = compute_surrogate_zscore(data_value, surrogates)

    if plot:
        plot_surrogates(surrogates, data_value, p_val, **plt_kwargs)

    if verbose:
        print('p-value: {:4.2f}'.format(p_val))
        print('z-score: {:4.2f}'.format(z_score))

    return p_val, z_score
