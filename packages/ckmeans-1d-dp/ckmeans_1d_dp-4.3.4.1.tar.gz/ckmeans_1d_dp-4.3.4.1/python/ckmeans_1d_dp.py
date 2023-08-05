from typing import NamedTuple
import numpy as np
import _ckmeans_1d_dp

    
class CKMeansResult(NamedTuple):
    cluster: np.ndarray
    centers: np.ndarray
    withinss: np.ndarray
    size: np.ndarray
    totss: float
    tot_withinss: float
    betweensss: float


def ckmeans(x, k=(1, 9), y=1, method='linear', estimate_k='BIC', dissimilarity='L2'):
    """ Perform optimal univariate k-means or k-median clustering in linear (fastest),
    loglinear, or quadratic (slowest) time.
    
    Parameters
    ----------
    x : array_like
        a numeric vector of data to be clustered. All `NaN` elements must be removed from `x`
        before calling this function. The function will run faster on sorted `x`
        (in non-decreasing order) than an unsorted input.
        
    k : int or (int, int)
        either an exact integer number of clusters, or a vector of length two specifying the
        minimum and maximum numbers of clusters to be examined. The default is `(1,9)`. When
        `k` is a range, the actual number of clusters is determined by Bayesian information 
        criterion.
        
    y : array_like
        a value of 1 (default) to specify equal weights of 1 for each element in `x`, or a
        numeric vector of unequal non-negative weights for each element in `x`. It is highly
        recommended to use positive (instead of zero) weights to account for the influence of
        every element. The weights have a strong impact on the clustering result. When the number
        of clusters `k` is given as a range, the weights should be linearly scaled to sum up
        to the observed sample size. Currently, kmedians only works with an equal weight
        of 1.
    
    method : {'linear', 'loglinear', 'quadratic'}
        a character string to specify the speedup method to the original cubic runtime dynamic
        programming. The default is "linear". All methods generate the same optimal results but
        differ in runtime or memory usage. See Details.
        
    estimate_k : {'BIC', 'BIC 3.4.12'}
        a character string to specify the method to estimate optimal `k`. This argument is
        effective only when a range for `k` is provided. The default is "BIC". See Details.
        
    dissimilarity : {'L2', 'L1', 'L2Y'}
        if 'L2' (default) then kmeans is performed. If 'L1', then kmedians is done instead.
        If 'L2Y' then preform ksegments.
    
    Returns
    -------
    cluster : ndarray
        a vector of clusters assigned to each element in `x`. 
        Each cluster is indexed by an integer from 0 to `k-1`.
        
    centers : ndarray
        a numeric vector of the (weighted) means for each cluster.
        
    withinss : ndarray
        a numeric vector of the (weighted) within-cluster sum of squares for each cluster.
        
    size : ndarray
        a vector of the (weighted) number of elements in each cluster.
        
    totss : float
        total sum of (weighted) squared distances between each element and the sample mean.
        This statistic is not dependent on the clustering result.
        
    tot_withinss : float
        total sum of (weighted) within-cluster squared distances between each element and
        its cluster mean. This statistic is minimized given the number of clusters.
        
    betweenss : float
        sum of (weighted) squared distances between each cluster mean and sample mean.
        This statistic is maximized given the number of clusters.
        
    Notes
    -----
    The original library returns clusters numbered 1 to `k`, which makes sinse in the
    1-indexed world of R. In Python, it makes more sense to use a zero index, so the
    clusters are instead nubmered 0 to `k-1`.
    """
    
    if type(k) == int:
        k_min = k_max = k
    else:
        k_min, k_max = k
    
    x = np.asarray(x)
    y = np.asarray(y)
    shape = x.shape
    
    k_shape = (*shape[:-1], k_max)
    bic_shape = (*shape[:-1], k_max-k_min+1)
    
    cluster = np.zeros_like(x, dtype='int32')
    centers = np.zeros(k_shape, dtype=float)
    withinss = np.zeros(k_shape, dtype=float)
    size = np.zeros(k_shape, dtype=float)
    BIC = np.zeros(bic_shape, dtype=float)
    
    _ckmeans_1d_dp.ckmeans(
        x, y, k_min, k_max,
        cluster, centers, withinss, size, BIC,
        estimate_k, method, dissimilarity
    )
    
    k_opt = 1+cluster.max(axis=-1)
    
    if y.size == x.size and y.any() and dissimilarity != 'L2Y':
        totss = np.average((x-np.average(x, weights=y, axis=-1))**2, weights=y, axis=-1)
    elif dissimilarity == 'L2Y':
        totss = y.var(axis=-1)*y.shape[-1]
    else:
        totss = x.var(axis=-1)*x.shape[-1]
    
    tot_withinss = withinss.sum(axis=-1) #possible error here
    betweenss = totss - tot_withinss
    
    return CKMeansResult(
        cluster=cluster,
        centers=centers,
        withinss=withinss,
        size=size,
        totss=totss,
        tot_withinss=tot_withinss,
        betweenss=betweenss,
    )
    