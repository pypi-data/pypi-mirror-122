import pandas as pd
import numpy as np
import functools


def tmm_norm_factors(data, trim_lfc=0.3, trim_mag=0.05, index_ref=None):
    """
    Compute Trimmed Means of M-values norm factors.

    Parameters
    ----------
    data : array_like
        Counts dataframe/Count data to normalize (rows are genes). Most often can be either
        pandas DataFrame or an numpy matrix.
    trim_lfc : float, optional
        Quantile cutoff for M_g (logfoldchanges). The default is 0.3.
    trim_mag : float, optional
        Quantile cutoff for A_g (log magnitude). The default is 0.05.
    index_ref : float, str, optional
        Reference index or column name to use as reference in the TMM
        algorithm. The default is None.

    Returns
    -------
    tmms : np.ndarray or pd.DataFrame
        Norm factors.

    """
    
    x = np.array(data, dtype=float).T
    lib_size = x.sum(axis=1)
    mask = x == 0
    if index_ref is None:
        x[:, np.all(mask, axis=0)] = np.nan
        p75 = np.nanpercentile(x, 75, axis=1)
        index_ref = np.argmin(abs(p75 - p75.mean()))
    mask[:, mask[index_ref]] = True
    x[mask] = np.nan
    with np.errstate(invalid='ignore', divide='ignore'):
        norm_x = x / lib_size[:, np.newaxis]
        logs = np.log2(norm_x)
        m_g =  logs - logs[index_ref]
        a_g = (logs + logs[index_ref]) / 2

        perc_m_g = np.nanquantile(m_g, [trim_lfc, 1 - trim_lfc], axis=1,
                                  interpolation='nearest')[..., np.newaxis]
        perc_a_g = np.nanquantile(a_g, [trim_mag, 1 - trim_mag], axis=1,
                                  interpolation='nearest')[..., np.newaxis]
        mask |= (m_g < perc_m_g[0]) | (m_g > perc_m_g[1])
        mask |= (a_g < perc_a_g[0]) | (a_g > perc_a_g[1])
        w_gk = (1 - norm_x) / x
        w_gk = 1 / (w_gk + w_gk[index_ref])
    w_gk[mask] = 0
    m_g[mask] = 0
    w_gk /= w_gk.sum(axis=1)[:, np.newaxis]
    tmms = np.sum(w_gk * m_g, axis=1)
    tmms -= tmms.mean()
    tmms = 2 ** tmms
    if type(data) is pd.DataFrame:
        tmms = pd.DataFrame(tmms, index=data.columns,
                            columns=['norm.factors'])
    return tmms


def tmm(data, trim_lfc=0.3, trim_mag=0.05, index_ref=None,
        return_norm_factors=False):
    """
    Normalize counts matrix by Trimmed Means of M-values (TMM).

    Parameters
    ----------
    data : array_like
        Counts dataframe/Count data to normalize (rows are genes). Most often can be either
        pandas DataFrame or an numpy matrix.
    trim_lfc : float, optional
        Quantile cutoff for M_g (logfoldchanges). The default is 0.3.
    trim_mag : float, optional
        Quantile cutoff for A_g (log magnitude). The default is 0.05.
    index_ref : float, str, optional
        Reference index or column name to use as reference in the TMM
        algorithm. The default is None.
    return_norm_factors : bool, optional
        If True, then norm factors are also returned. The default is False.

    Returns
    -------
    data : array_like
        Normalized data.

    """
    
    nf = tmm_norm_factors(data, trim_lfc=trim_lfc, trim_mag=trim_mag,
                          index_ref=index_ref)
    if return_norm_factors:
        return data / np.array(nf).flatten(), nf
    return data / np.array(nf).flatten()


def scaler(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        nf = kwargs.get('norm_factors')
        r = fun(*args, **kwargs)
        if nf is not None:
            if type(nf) is str and nf == 'TMM':
                nf = tmm_norm_factors(args[0])
            r /= np.array(nf).flatten()
        return r
    return wrapper


@scaler
def total_count(matrix, norm_factors=None):
    """
    Total count normalization.
    
    
    Parameters
    ----------
    matrix : array_like
        Count data to normalize (rows are genes).
    norm_factors : array_like, optional
        Normalized factors to apply before doing CPM. Can also be a string
        'TMM' - then, norm factors are computed automatically. If None,
        then no norm factors are applied. The default is None.

    Returns
    -------
    array_like
        Normalized matrix.
    """
    return matrix / matrix.sum(axis=0)


def cpm(matrix, val=1e6, norm_factors=None):
    """
    Counts per million normalization.

    Total count normalization + multiplication by a million.
    Parameters
    ----------
    matrix : array_like
        Count data to normalize (rows are genes).
    val : float, optional
        Custom value to multiply afterwards. The default is 1e6.
    norm_factors : array_like, optional
        Normalized factors to apply before doing CPM. Can also be a string
        'TMM' - then, norm factors are computed automatically. If None,
        then no norm factors are applied. The default is None.

    Returns
    -------
    array_like
        Normalized matrix.

    """
    return total_count(matrix, norm_factors=norm_factors) * 1e6
    

@scaler
def percentile(matrix, p, norm_factors=None):
    """
    Percentile normalization
    
    Parameters
    ----------
    matrix : array_like
        Count data to normalize (rows are genes).
    p : float in range of [0,100]
        Percentile to compute, which must be between 0 and 100 inclusive.
    norm_factors : array_like
        Normalized factors to apply before doing CPM. Can also be a string
        'TMM' - then, norm factors are computed automatically. If None,
        then no norm factors are applied. The default is None.
        
    Returns
    -------
    array_like
        Normalized matrix.
    """
    return matrix / np.percentile(matrix[np.any(matrix > 0, axis=1)], p,
                                  axis=0, interpolation='nearest')


def quartile(matrix, q, norm_factors=None):
    """
    Quartile normalization.
    
    A wrapper around percentile normalization.
    Parameters
    ----------
    matrix : array_like
        Matrix or dataframe to normalize.
    q : str, int
        Quartile number or name. Can be either {"lower", "median", "upper"} or
       {1, 2, 3}.
    norm_factors : array_like
        Normalized factors to apply before doing CPM. Can also be a string
        'TMM' - then, norm factors are computed automatically. If None,
        then no norm factors are applied. The default is None.

    Returns
    -------
    array_like
        Normalized matrix.
    """
    d = {"upper": 75, "lower": 25, "median": 50, 3: 75, 1: 25, 2: 50}
    assert q in d, f'Unkown quartile name: {q}'
    return percentile(matrix, d[q], norm_factors=norm_factors)


@scaler
def rpk(matrix, length: str, norm_factors=None):
    """
    Reads per kilobase normalization.

    Counts are divided by a gene length.
    Parameters
    ----------
    matrix : array_like
        Count data to normalize (rows are genes).
    length : str
        Column name (if matrix is Pandas DataFrame), column index (if matrix
        is a numpy array) or an array, where gene lengths are stored.
    norm_factors : array_like, optional
        Normalized factors to apply before doing CPM. Can also be a string
        'TMM' - then, norm factors are computed automatically. If None,
        then no norm factors are applied. The default is None.

    Returns
    -------
    array_like
        Normalized matrix.

    """
    if type(length) is str:
        tlen = length
        length = np.array(matrix[length])
        matrix = matrix.drop(tlen, axis=1)
    elif type(length) is int:
        length = matrix[:, length]
    elif type(length) is pd.DataFrame:
        length = length.loc[matrix.index]
    length = np.array(length).reshape(-1, 1) / 1000
    return matrix / length

def rpkm(matrix, length: str, val=1e6, norm_factors=None):
    """
    Reads per kilobase normalization per million.

    Counts are divided by a gene length and multiplied by a million.
    Parameters
    ----------
    matrix : array_like
        Count data to normalize (rows are genes).
    length : str
        Column name (if matrix is Pandas DataFrame), column index (if matrix
        is a numpy array) or an array, where gene lengths are stored.
    val : float, optional
        Custom value to multiply afterwards. The default is 1e6.
    norm_factors : array_like, optional
        Normalized factors to apply before doing CPM. Can also be a string
        'TMM' - then, norm factors are computed automatically. If None,
        then no norm factors are applied. The default is None.

    Returns
    -------
    array_like
        Normalized matrix.

    """
    return rpk(matrix, length, norm_factors) * val


def getmm(matrix, length: str, trim_lfc=0.3, trim_mag=0.05, index_ref=None):
    """
    GeTMM normalization (RPK + TMM).

    Parameters
    ----------
    matrix : array_like
        Count data to normalize (rows are genes).
    length : str
        Column name (if matrix is Pandas DataFrame), column index (if matrix
        is a numpy array) or an array, where gene lengths are stored.
    trim_lfc : float, optional
        Quantile cutoff for M_g (logfoldchanges). The default is 0.3.
    trim_mag : float, optional
        Quantile cutoff for A_g (log magnitude). The default is 0.05.
    index_ref : float, str, optional
        Reference index or column name to use as reference in the TMM
        algorithm. The default is None.

    Returns
    -------
    array_like
        Normalized matrix.

    """
    matrix = rpk(matrix, length)
    return tmm(matrix, trim_lfc=trim_lfc, trim_mag=trim_mag,
               index_ref=index_ref)
    
