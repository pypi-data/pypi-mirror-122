import pandas as pd
import numpy as np


def tmm_norm_factors(data, trim_lfc=0.3, trim_mag=0.05, index_ref=None):
    """
    Compute Trimmed Means of M-values norm factors.

    Parameters
    ----------
    data : array_like
        Counts dataframe/matrix to normalize. Most often can be either
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
        Counts dataframe/matrix to normalize. Most often can be either
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


def total_count(matrix):
    """
    Total count normalization.
    
    
    Parameters
    ----------
    matrix : array_like
        Matrix to normalize.
        
    Returns
    -------
    array_like
        Normalized matrix.
    """
    return matrix / matrix.sum(axis=0)


def cpm(matrix, norm_factors=None, val=1e6):
    """
    Counts per million normalization.

    Total count normalization + multiplication by a million.
    Parameters
    ----------
    matrix : array_like
        Count data to normalize.
    norm_factors : array_like
        Normalized factors to apply before doing CPM. Can also be a string
        'TMM' - then, norm factors are computed automatically. If None,
        then no norm factors are applied. The default is None.
    val : float, optional
        Custom value to multiply afterwards. The default is 1e6.

    Returns
    -------
    None.

    """
    if type(norm_factors) is str and norm_factors == 'TMM':
        norm_factors = tmm_norm_factors(matrix)
    res = total_count(matrix) * val
    if norm_factors is not None:
        res /= np.array(norm_factors).flatten()
    return res
    

def percentile(matrix, p, saving_memory=False):
    """
    Percentile normalization
    
    Parameters
    ----------
    matrix : array_like
        Matrix to normalize.
    p : float in range of [0,100]
        Percentile to compute, which must be between 0 and 100 inclusive.
    saving_memory : bool
        Parameter for activation of RAM saving mode. This may take longer.
        
    Returns
    -------
    array_like
        Normalized matrix.
    """
    return matrix / np.percentile(matrix[np.any(matrix > 0, axis=1)], p,
                                  axis=0, interpolation='nearest')


def quartile(matrix, q, saving_memory=False):
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

    Returns
    -------
    array_like
        Normalized matrix.
    """
    d = {"upper": 75, "lower": 25, "median": 50, 3: 75, 1: 25, 2: 50}
    assert q in d, f'Unkown quartile name: {q}'
    return percentile(matrix, d[q])
