import pytest
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from anndata import AnnData
from ..utils_anndata import get_acts, swap_layer, extract_psbulk_inputs, check_for_raw_counts
from ..utils_anndata import format_psbulk_inputs, psbulk_profile, compute_psbulk, get_unq_dict, get_pseudobulk
from ..utils_anndata import check_if_skip, get_contrast, get_top_targets, format_contrast_results


def test_get_acts():
    m = np.array([[1, 0, 2], [1, 0, 3], [0, 0, 0]])
    r = np.array(['S1', 'S2', 'S3'])
    c = np.array(['G1', 'G2', 'G3'])
    df = pd.DataFrame(m, index=r, columns=c)
    estimate = pd.DataFrame([[3.5, -0.5], [3.6, -0.6], [-1, 2]],
                            columns=['T1', 'T2'], index=r)
    adata = AnnData(df, dtype=np.float32)
    adata.obsm['estimate'] = estimate
    acts = get_acts(adata, 'estimate')
    assert acts.shape[0] == adata.shape[0]
    assert acts.shape[1] != adata.shape[1]
    assert np.any(acts.X < 0)
    assert not np.any(adata.X < 0)


def test_swap_layer():
    m = np.array([[1, 0, 2], [1, 0, 3], [0, 0, 1]])
    r = np.array(['S1', 'S2', 'S3'])
    c = np.array(['G1', 'G2', 'G3'])
    df = pd.DataFrame(m, index=r, columns=c)
    adata = AnnData(df, dtype=np.float32)
    adata.layers['norm'] = adata.X / np.sum(adata.X, axis=1).reshape(-1, 1)
    sdata = swap_layer(adata, 'norm')
    assert not np.all(np.mod(sdata.X, 1) == 0)
    swap_layer(adata=adata, layer_key='norm', inplace=True)
    assert not np.all(np.mod(adata.X, 1) == 0)
    assert adata.layers['X'] is not None


def test_extract_psbulk_inputs():
    m = np.array([[1, 0, 2], [1, 0, 3], [0, 0, 0]])
    r = np.array(['S1', 'S2', 'S3'])
    c = np.array(['G1', 'G2', 'G3'])
    df = pd.DataFrame(m, index=r, columns=c)
    obs = pd.DataFrame([['C01', 'C01', 'C02']], columns=r, index=['celltype']).T
    adata = AnnData(df, obs=obs, dtype=np.float32)
    adata.layers['counts'] = adata.X
    adata_raw = adata.copy()
    adata_raw.raw = adata_raw
    extract_psbulk_inputs(adata, obs=None, layer='counts', use_raw=False)
    extract_psbulk_inputs(adata, obs=None, layer=None, use_raw=False)
    extract_psbulk_inputs(adata_raw, obs=None, layer=None, use_raw=True)
    extract_psbulk_inputs(df, obs=obs, layer=None, use_raw=False)
    with pytest.raises(ValueError):
        extract_psbulk_inputs(adata, obs=None, layer=None, use_raw=True)
    with pytest.raises(ValueError):
        extract_psbulk_inputs(df, obs=None, layer=None, use_raw=False)


def test_check_for_raw_counts():
    X = csr_matrix(np.array([[1, 0, 2], [1, 0, 3], [0, 0, 0]]))
    X_float = csr_matrix(np.array([[1.3, 0, 2.1], [1.48, 0.123, 3.33], [0, 0, 0]]))
    X_neg = csr_matrix(np.array([[1, 0, -2], [1, 0, -3], [0, 0, 0]]))
    X_inf = csr_matrix(np.array([[1, 0, np.nan], [1, 0, 3], [0, 0, 0]]))
    check_for_raw_counts(X)
    with pytest.raises(ValueError):
        check_for_raw_counts(X_float)
    with pytest.raises(ValueError):
        check_for_raw_counts(X_neg)
    with pytest.raises(ValueError):
        check_for_raw_counts(X_inf)
    check_for_raw_counts(X_float, skip_checks=True)
    check_for_raw_counts(X_neg, skip_checks=True)
    with pytest.raises(ValueError):
        check_for_raw_counts(X_inf, skip_checks=True)


def test_format_psbulk_inputs():
    sample_col, groups_col = 'sample_id', 'celltype'
    obs = pd.DataFrame([['S1', 'S2', 'S3'], ['C1', 'C1', 'C2']], columns=['S1', 'S2', 'S3'], index=[sample_col, groups_col]).T
    format_psbulk_inputs(sample_col, groups_col, obs)
    format_psbulk_inputs(sample_col, None, obs)


def test_psbulk_profile():
    profile = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ])
    p = psbulk_profile(profile, mode='sum')
    assert np.all(p == np.array([12, 15, 18]))
    p = psbulk_profile(profile, mode='mean')
    assert np.all(p == np.array([4, 5, 6]))
    p = psbulk_profile(profile, mode='median')
    assert np.all(p == np.array([4, 5, 6]))
    with pytest.raises(ValueError):
        psbulk_profile(profile, mode='mode')


def test_compute_psbulk():
    sample_col, groups_col = 'sample_id', 'celltype'
    min_cells, min_counts, min_prop = 0., 0., 0.
    X = csr_matrix(np.array([[1, 0, 2], [1, 0, 3], [0, 0, 0]]))
    smples = np.array(['S1', 'S1', 'S2'])
    groups = np.array(['C1', 'C1', 'C1'])
    n_rows = len(smples)
    n_cols = X.shape[1]
    psbulk = np.zeros((n_rows, n_cols))
    props = np.full((n_rows, n_cols), False)
    obs = pd.DataFrame([smples, groups], columns=smples, index=[sample_col, groups_col]).T
    new_obs = pd.DataFrame(columns=obs.columns)
    compute_psbulk(psbulk, props, X, sample_col, groups_col, np.unique(smples),
                   np.unique(groups), obs, new_obs, min_cells, min_counts, min_prop, 'sum')
    compute_psbulk(psbulk, props, X, sample_col, None, np.unique(smples),
                   np.unique(groups), obs, new_obs, min_cells, min_counts, min_prop, 'sum')


def test_get_pseudobulk():
    sample_col, groups_col = 'sample_id', 'celltype'
    m = np.array([[6, 0, 1], [2, 0, 2], [1, 3, 3], [0, 1, 1], [1, 0, 1]])
    r = np.array(['B1', 'B2', 'B3', 'B4', 'B5'])
    c = np.array(['G1', 'G2', 'G3'])
    df = pd.DataFrame(m, index=r, columns=c)
    smples = np.array(['S1', 'S1', 'S1', 'S2', 'S2'])
    groups = np.array(['C1', 'C1', 'C1', 'C1', 'C2'])
    obs = pd.DataFrame([smples, groups], columns=r, index=[sample_col, groups_col]).T
    adata = AnnData(df, obs=obs, dtype=np.float32)
    pdata = get_pseudobulk(adata, sample_col, sample_col, min_prop=0, min_cells=0, min_counts=0, min_smpls=0)
    assert pdata.shape[0] == 2
    pdata = get_pseudobulk(adata, sample_col, groups_col, min_prop=0, min_cells=0, min_counts=0, min_smpls=0, mode='sum')
    assert pdata.shape[0] == 3
    assert np.all(pdata.X[0] == np.array([9., 3., 6.]))
    pdata = get_pseudobulk(adata, sample_col, groups_col, min_prop=0, min_cells=0, min_counts=0, min_smpls=0, mode='mean')
    assert pdata.shape[0] == 3
    assert np.all(pdata.X[0] == np.array([3., 1., 2.]))
    pdata = get_pseudobulk(adata, sample_col, groups_col, min_prop=0, min_cells=0, min_counts=0, min_smpls=0, mode='median')
    assert pdata.shape[0] == 3
    assert np.all(pdata.X[0] == np.array([2., 0., 2.]))


def test_get_unq_dict():
    col = pd.Series(['C1', 'C1', 'C2', 'C3'], index=['S1', 'S2', 'S3', 'S4'])
    condition = 'C1'
    reference = 'C2'
    get_unq_dict(col, condition, reference)
    get_unq_dict(col, condition, 'rest')


def test_check_if_skip():
    grp = 'Group'
    condition_col = 'celltype'
    condition = 'C1'
    reference = 'C2'
    unq_dict = {'C1': 2}
    check_if_skip(grp, condition_col, condition, reference, unq_dict)
    unq_dict = {'C2': 2}
    check_if_skip(grp, condition_col, condition, reference, unq_dict)
    unq_dict = {'C1': 2, 'C2': 1}
    check_if_skip(grp, condition_col, condition, reference, unq_dict)
    unq_dict = {'C1': 1, 'C2': 2}
    check_if_skip(grp, condition_col, condition, reference, unq_dict)


def test_get_contrast():
    groups_col, condition_col = 'celltype', 'condition'
    m = np.array([[7., 1., 1.], [4., 2., 1.], [1., 2., 5.], [1., 1., 6.]])
    r = np.array(['S1', 'S2', 'S3', 'S4'])
    c = np.array(['G1', 'G2', 'G3'])
    df = pd.DataFrame(m, index=r, columns=c)
    condition = 'Ds'
    reference = 'Ht'
    obs = pd.DataFrame([['C1', 'C1', 'C1', 'C1'], [condition, condition, reference, reference]],
                       columns=r, index=[groups_col, condition_col]).T
    adata = AnnData(df, obs=obs, dtype=np.float32)
    get_contrast(adata, groups_col, condition_col, condition, None)
    get_contrast(adata, groups_col, condition_col, condition, reference)
    get_contrast(adata, None, condition_col, condition, reference)
    with pytest.raises(ValueError):
        get_contrast(adata, groups_col, condition_col, condition, condition)
    obs = pd.DataFrame([['C1', 'C1', 'C1', 'C1'], [condition, condition, condition, reference]],
                       columns=r, index=[groups_col, condition_col]).T
    get_contrast(adata, groups_col, condition_col, condition, reference)


def test_get_top_targets():
    logFCs = pd.DataFrame([[3, 0, -3], [1, 2, -5]], index=['C1', 'C2'], columns=['G1', 'G2', 'G3'])
    pvals = pd.DataFrame([[.3, .02, .01], [.9, .1, .003]], index=['C1', 'C2'], columns=['G1', 'G2', 'G3'])
    contrast = 'C1'
    name = 'T1'
    net = pd.DataFrame([['T1', 'G1', 1], ['T1', 'G2', 1], ['T2', 'G3', 1], ['T2', 'G4', 0.5]],
                       columns=['source', 'target', 'weight'])
    get_top_targets(logFCs, pvals, contrast, name=name, net=net, sign_thr=1, lFCs_thr=0.0, fdr_corr=True)
    with pytest.raises(ValueError):
        get_top_targets(logFCs, pvals, contrast, name=None, net=net, sign_thr=1, lFCs_thr=0.0, fdr_corr=True)
    get_top_targets(logFCs, pvals, contrast, name=None, net=None, sign_thr=1, lFCs_thr=0.0, fdr_corr=True)
    get_top_targets(logFCs, pvals, contrast, name=None, net=None, sign_thr=1, lFCs_thr=0.0, fdr_corr=False)


def test_format_contrast_results():
    logFCs = pd.DataFrame([[3, 0, -3], [1, 2, -5]], index=['C1', 'C2'], columns=['G1', 'G2', 'G3'])
    logFCs.name = 'contrast_logFCs'
    pvals = pd.DataFrame([[.3, .02, .01], [.9, .1, .003]], index=['C1', 'C2'], columns=['G1', 'G2', 'G3'])
    pvals.name = 'contrast_pvals'
    format_contrast_results(logFCs, pvals)
