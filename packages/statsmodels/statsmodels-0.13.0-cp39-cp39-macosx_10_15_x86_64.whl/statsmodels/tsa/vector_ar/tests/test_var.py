# -*- coding: utf-8 -*-
"""
Test VAR Model
"""
from statsmodels.compat.pandas import assert_index_equal
from statsmodels.compat.python import lrange

from io import BytesIO, StringIO
import os
import sys
import warnings

import numpy as np
from numpy.testing import assert_allclose, assert_almost_equal, assert_equal
import pandas as pd
import pytest

from statsmodels.datasets import macrodata
import statsmodels.tools.data as data_util
from statsmodels.tools.sm_exceptions import ValueWarning
from statsmodels.tsa.base.datetools import dates_from_str
import statsmodels.tsa.vector_ar.util as util
from statsmodels.tsa.vector_ar.var_model import VAR, var_acf

DECIMAL_12 = 12
DECIMAL_6 = 6
DECIMAL_5 = 5
DECIMAL_4 = 4
DECIMAL_3 = 3
DECIMAL_2 = 2


@pytest.fixture()
def bivariate_var_data(reset_randomstate):
    """A bivariate dataset for VAR estimation"""
    e = np.random.standard_normal((252, 2))
    y = np.zeros_like(e)
    y[:2] = e[:2]
    for i in range(2, 252):
        y[i] = 0.2 * y[i - 1] + 0.1 * y[i - 2] + e[i]
    return y


@pytest.fixture()
def bivariate_var_result(bivariate_var_data):
    """A bivariate VARResults for reuse"""
    mod = VAR(bivariate_var_data)
    return mod.fit()


class CheckVAR(object):  # FIXME: not inherited, so these tests are never run!
    # just so pylint will not complain
    res1 = None
    res2 = None

    def test_params(self):
        assert_almost_equal(self.res1.params, self.res2.params, DECIMAL_3)

    def test_neqs(self):
        assert_equal(self.res1.neqs, self.res2.neqs)

    def test_nobs(self):
        assert_equal(self.res1.avobs, self.res2.nobs)

    def test_df_eq(self):
        assert_equal(self.res1.df_eq, self.res2.df_eq)

    def test_rmse(self):
        results = self.res1.results
        for i in range(len(results)):
            assert_almost_equal(
                results[i].mse_resid ** 0.5,
                eval("self.res2.rmse_" + str(i + 1)),
                DECIMAL_6,
            )

    def test_rsquared(self):
        results = self.res1.results
        for i in range(len(results)):
            assert_almost_equal(
                results[i].rsquared,
                eval("self.res2.rsquared_" + str(i + 1)),
                DECIMAL_3,
            )

    def test_llf(self):
        results = self.res1.results
        assert_almost_equal(self.res1.llf, self.res2.llf, DECIMAL_2)
        for i in range(len(results)):
            assert_almost_equal(
                results[i].llf, eval("self.res2.llf_" + str(i + 1)), DECIMAL_2
            )

    def test_aic(self):
        assert_almost_equal(self.res1.aic, self.res2.aic)

    def test_bic(self):
        assert_almost_equal(self.res1.bic, self.res2.bic)

    def test_hqic(self):
        assert_almost_equal(self.res1.hqic, self.res2.hqic)

    def test_fpe(self):
        assert_almost_equal(self.res1.fpe, self.res2.fpe)

    def test_detsig(self):
        assert_almost_equal(self.res1.detomega, self.res2.detsig)

    def test_bse(self):
        assert_almost_equal(self.res1.bse, self.res2.bse, DECIMAL_4)


def get_macrodata():
    data = macrodata.load_pandas().data[["realgdp", "realcons", "realinv"]]
    data = data.to_records(index=False)
    nd = data.view((float, 3), type=np.ndarray)
    nd = np.diff(np.log(nd), axis=0)
    return nd.ravel().view(data.dtype, type=np.ndarray)


def generate_var():  # FIXME: make a test?
    import pandas.rpy.common as prp
    from rpy2.robjects import r

    r.source("tests/var.R")
    return prp.convert_robj(r["result"], use_pandas=False)


def write_generate_var():  # FIXME: make a test?
    result = generate_var()
    np.savez("tests/results/vars_results.npz", **result)


class RResults(object):
    """
    Simple interface with results generated by "vars" package in R.
    """

    def __init__(self):
        # data = np.load(resultspath + 'vars_results.npz')
        from .results.results_var_data import var_results

        data = var_results.__dict__

        self.names = data["coefs"].dtype.names
        self.params = data["coefs"].view(
            (float, len(self.names)), type=np.ndarray
        )
        self.stderr = data["stderr"].view(
            (float, len(self.names)), type=np.ndarray
        )

        self.irf = data["irf"].item()
        self.orth_irf = data["orthirf"].item()

        self.nirfs = int(data["nirfs"][0])
        self.nobs = int(data["obs"][0])
        self.totobs = int(data["totobs"][0])

        crit = data["crit"].item()
        self.aic = crit["aic"][0]
        self.sic = self.bic = crit["sic"][0]
        self.hqic = crit["hqic"][0]
        self.fpe = crit["fpe"][0]

        self.detomega = data["detomega"][0]
        self.loglike = data["loglike"][0]

        self.nahead = int(data["nahead"][0])
        self.ma_rep = data["phis"]

        self.causality = data["causality"]


_orig_stdout = None


def setup_module():
    global _orig_stdout
    _orig_stdout = sys.stdout
    sys.stdout = StringIO()


class CheckIRF(object):
    ref = None
    res = None
    irf = None
    k = None

    # ---------------------------------------------------------------------------
    # IRF tests

    def test_irf_coefs(self):
        self._check_irfs(self.irf.irfs, self.ref.irf)
        self._check_irfs(self.irf.orth_irfs, self.ref.orth_irf)

    def _check_irfs(self, py_irfs, r_irfs):
        for i, name in enumerate(self.res.names):
            ref_irfs = r_irfs[name].view((float, self.k), type=np.ndarray)
            res_irfs = py_irfs[:, :, i]
            assert_almost_equal(ref_irfs, res_irfs)

    @pytest.mark.matplotlib
    def test_plot_irf(self, close_figures):
        self.irf.plot()
        self.irf.plot(plot_stderr=False)

        self.irf.plot(impulse=0, response=1)
        self.irf.plot(impulse=0)
        self.irf.plot(response=0)

        self.irf.plot(orth=True)
        self.irf.plot(impulse=0, response=1, orth=True)

    @pytest.mark.matplotlib
    def test_plot_cum_effects(self, close_figures):
        self.irf.plot_cum_effects()
        self.irf.plot_cum_effects(plot_stderr=False)
        self.irf.plot_cum_effects(impulse=0, response=1)

        self.irf.plot_cum_effects(orth=True)
        self.irf.plot_cum_effects(impulse=0, response=1, orth=True)

    @pytest.mark.matplotlib
    def test_plot_figsizes(self):
        assert_equal(self.irf.plot().get_size_inches(), (10, 10))
        assert_equal(
            self.irf.plot(figsize=(14, 10)).get_size_inches(), (14, 10)
        )

        assert_equal(self.irf.plot_cum_effects().get_size_inches(), (10, 10))
        assert_equal(
            self.irf.plot_cum_effects(figsize=(14, 10)).get_size_inches(),
            (14, 10),
        )


@pytest.mark.smoke
class CheckFEVD(object):
    fevd = None

    # ---------------------------------------------------------------------------
    # FEVD tests

    @pytest.mark.matplotlib
    def test_fevd_plot(self, close_figures):
        self.fevd.plot()

    def test_fevd_repr(self):
        self.fevd

    def test_fevd_summary(self):
        self.fevd.summary()

    @pytest.mark.xfail(
        reason="FEVD.cov() is not implemented",
        raises=NotImplementedError,
        strict=True,
    )
    def test_fevd_cov(self):
        # test does not crash
        # not implemented
        covs = self.fevd.cov()
        raise NotImplementedError


class TestVARResults(CheckIRF, CheckFEVD):
    @classmethod
    def setup_class(cls):
        cls.p = 2

        cls.data = get_macrodata()
        cls.model = VAR(cls.data)
        cls.names = cls.model.endog_names

        cls.ref = RResults()
        cls.k = len(cls.ref.names)
        cls.res = cls.model.fit(maxlags=cls.p)

        cls.irf = cls.res.irf(cls.ref.nirfs)
        cls.nahead = cls.ref.nahead

        cls.fevd = cls.res.fevd()

    def test_constructor(self):
        # make sure this works with no names
        ndarr = self.data.view((float, 3), type=np.ndarray)
        model = VAR(ndarr)
        res = model.fit(self.p)

    def test_names(self):
        assert_equal(self.model.endog_names, self.ref.names)

        model2 = VAR(self.data)
        assert_equal(model2.endog_names, self.ref.names)

    def test_get_eq_index(self):
        assert type(self.res.names) is list  # noqa: E721

        for i, name in enumerate(self.names):
            idx = self.res.get_eq_index(i)
            idx2 = self.res.get_eq_index(name)

            assert_equal(idx, i)
            assert_equal(idx, idx2)

        with pytest.raises(Exception):
            self.res.get_eq_index("foo")

    @pytest.mark.smoke
    def test_repr(self):
        # just want this to work
        foo = str(self.res)
        bar = repr(self.res)

    def test_params(self):
        assert_almost_equal(self.res.params, self.ref.params, DECIMAL_3)

    @pytest.mark.smoke
    def test_cov_params(self):
        # do nothing for now
        self.res.cov_params

    @pytest.mark.smoke
    def test_cov_ybar(self):
        self.res.cov_ybar()

    @pytest.mark.smoke
    def test_tstat(self):
        self.res.tvalues

    @pytest.mark.smoke
    def test_pvalues(self):
        self.res.pvalues

    @pytest.mark.smoke
    def test_summary(self):
        summ = self.res.summary()

    def test_detsig(self):
        assert_almost_equal(self.res.detomega, self.ref.detomega)

    def test_aic(self):
        assert_almost_equal(self.res.aic, self.ref.aic)

    def test_bic(self):
        assert_almost_equal(self.res.bic, self.ref.bic)

    def test_hqic(self):
        assert_almost_equal(self.res.hqic, self.ref.hqic)

    def test_fpe(self):
        assert_almost_equal(self.res.fpe, self.ref.fpe)

    def test_lagorder_select(self):
        ics = ["aic", "fpe", "hqic", "bic"]

        for ic in ics:
            res = self.model.fit(maxlags=10, ic=ic, verbose=True)

        with pytest.raises(Exception):
            self.model.fit(ic="foo")

    def test_nobs(self):
        assert_equal(self.res.nobs, self.ref.nobs)

    def test_stderr(self):
        assert_almost_equal(self.res.stderr, self.ref.stderr, DECIMAL_4)

    def test_loglike(self):
        assert_almost_equal(self.res.llf, self.ref.loglike)

    def test_ma_rep(self):
        ma_rep = self.res.ma_rep(self.nahead)
        assert_almost_equal(ma_rep, self.ref.ma_rep)

    # --------------------------------------------------
    # Lots of tests to make sure stuff works...need to check correctness

    def test_causality(self):
        causedby = self.ref.causality["causedby"]

        for i, name in enumerate(self.names):
            variables = self.names[:i] + self.names[i + 1 :]
            result = self.res.test_causality(name, variables, kind="f")
            assert_almost_equal(result.pvalue, causedby[i], DECIMAL_4)

            rng = lrange(self.k)
            rng.remove(i)
            result2 = self.res.test_causality(i, rng, kind="f")
            assert_almost_equal(result.pvalue, result2.pvalue, DECIMAL_12)

            # make sure works
            result = self.res.test_causality(name, variables, kind="wald")

        # corner cases
        _ = self.res.test_causality(self.names[0], self.names[1])
        _ = self.res.test_causality(0, 1)

        with pytest.raises(Exception):
            self.res.test_causality(0, 1, kind="foo")

    def test_causality_no_lags(self):
        res = VAR(self.data).fit(maxlags=0)
        with pytest.raises(RuntimeError, match="0 lags"):
            res.test_causality(0, 1)

    @pytest.mark.smoke
    def test_select_order(self):
        result = self.model.fit(10, ic="aic", verbose=True)
        result = self.model.fit(10, ic="fpe", verbose=True)

        # bug
        model = VAR(self.model.endog)
        model.select_order()

    def test_is_stable(self):
        # may not necessarily be true for other datasets
        assert self.res.is_stable(verbose=True)

    def test_acf(self):
        # test that it works...for now
        acfs = self.res.acf(10)

        # defaults to nlags=lag_order
        acfs = self.res.acf()
        assert len(acfs) == self.p + 1

    def test_acf_2_lags(self):
        c = np.zeros((2, 2, 2))
        c[0] = np.array([[0.2, 0.1], [0.15, 0.15]])
        c[1] = np.array([[0.1, 0.9], [0, 0.1]])

        acf = var_acf(c, np.eye(2), 3)

        gamma = np.zeros((6, 6))
        gamma[:2, :2] = acf[0]
        gamma[2:4, 2:4] = acf[0]
        gamma[4:6, 4:6] = acf[0]
        gamma[2:4, :2] = acf[1].T
        gamma[4:, :2] = acf[2].T
        gamma[:2, 2:4] = acf[1]
        gamma[:2, 4:] = acf[2]
        recovered = np.dot(gamma[:2, 2:], np.linalg.inv(gamma[:4, :4]))
        recovered = [recovered[:, 2 * i : 2 * (i + 1)] for i in range(2)]
        recovered = np.array(recovered)
        assert_allclose(recovered, c, atol=1e-7)

    @pytest.mark.smoke
    def test_acorr(self):
        acorrs = self.res.acorr(10)

    @pytest.mark.smoke
    def test_forecast(self):
        self.res.forecast(self.res.endog[-5:], 5)

    @pytest.mark.smoke
    def test_forecast_interval(self):
        y = self.res.endog[: -self.p :]
        point, lower, upper = self.res.forecast_interval(y, 5)

    @pytest.mark.matplotlib
    def test_plot_sim(self, close_figures):
        self.res.plotsim(steps=100)

    @pytest.mark.matplotlib
    def test_plot(self, close_figures):
        self.res.plot()

    @pytest.mark.matplotlib
    def test_plot_acorr(self, close_figures):
        self.res.plot_acorr()

    @pytest.mark.matplotlib
    def test_plot_forecast(self, close_figures):
        self.res.plot_forecast(5)

    def test_reorder(self):
        # manually reorder
        data = self.data.view((float, 3), type=np.ndarray)
        names = self.names
        data2 = np.append(
            np.append(data[:, 2, None], data[:, 0, None], axis=1),
            data[:, 1, None],
            axis=1,
        )
        names2 = []
        names2.append(names[2])
        names2.append(names[0])
        names2.append(names[1])
        res2 = VAR(data2).fit(maxlags=self.p)

        # use reorder function
        res3 = self.res.reorder(["realinv", "realgdp", "realcons"])

        # check if the main results match
        assert_almost_equal(res2.params, res3.params)
        assert_almost_equal(res2.sigma_u, res3.sigma_u)
        assert_almost_equal(res2.bic, res3.bic)
        assert_almost_equal(res2.stderr, res3.stderr)

    def test_pickle(self):
        fh = BytesIO()
        # test wrapped results load save pickle
        del self.res.model.data.orig_endog
        self.res.save(fh)
        fh.seek(0, 0)
        res_unpickled = self.res.__class__.load(fh)
        assert type(res_unpickled) is type(self.res)  # noqa: E721


class E1_Results(object):
    """
    Results from Lütkepohl (2005) using E2 dataset
    """

    def __init__(self):
        # Lutkepohl p. 120 results

        # I asked the author about these results and there is probably rounding
        # error in the book, so I adjusted these test results to match what is
        # coming out of the Python (double-checked) calculations
        self.irf_stderr = np.array(
            [
                [
                    [0.125, 0.546, 0.664],
                    [0.032, 0.139, 0.169],
                    [0.026, 0.112, 0.136],
                ],
                [
                    [0.129, 0.547, 0.663],
                    [0.032, 0.134, 0.163],
                    [0.026, 0.108, 0.131],
                ],
                [
                    [0.084, 0.385, 0.479],
                    [0.016, 0.079, 0.095],
                    [0.016, 0.078, 0.103],
                ],
            ]
        )

        self.cum_irf_stderr = np.array(
            [
                [
                    [0.125, 0.546, 0.664],
                    [0.032, 0.139, 0.169],
                    [0.026, 0.112, 0.136],
                ],
                [
                    [0.149, 0.631, 0.764],
                    [0.044, 0.185, 0.224],
                    [0.033, 0.140, 0.169],
                ],
                [
                    [0.099, 0.468, 0.555],
                    [0.038, 0.170, 0.205],
                    [0.033, 0.150, 0.185],
                ],
            ]
        )

        self.lr_stderr = np.array(
            [
                [0.134, 0.645, 0.808],
                [0.048, 0.230, 0.288],
                [0.043, 0.208, 0.260],
            ]
        )


basepath = os.path.split(__file__)[0]
resultspath = os.path.join(basepath, "results")


def get_lutkepohl_data(name="e2"):
    path = os.path.join(resultspath, f"{name}.dat")

    return util.parse_lutkepohl_data(path)


def test_lutkepohl_parse():
    files = ["e%d" % i for i in range(1, 7)]

    for f in files:
        get_lutkepohl_data(f)


class TestVARResultsLutkepohl(object):
    """
    Verify calculations using results from Lütkepohl's book
    """

    @classmethod
    def setup_class(cls):
        cls.p = 2
        sdata, dates = get_lutkepohl_data("e1")

        data = data_util.struct_to_ndarray(sdata)
        adj_data = np.diff(np.log(data), axis=0)
        # est = VAR(adj_data, p=2, dates=dates[1:], names=names)

        cls.model = VAR(adj_data[:-16], dates=dates[1:-16], freq="BQ-MAR")
        cls.res = cls.model.fit(maxlags=cls.p)
        cls.irf = cls.res.irf(10)
        cls.lut = E1_Results()

    def test_approx_mse(self):
        # 3.5.18, p. 99
        mse2 = (
            np.array(
                [
                    [25.12, 0.580, 1.300],
                    [0.580, 1.581, 0.586],
                    [1.300, 0.586, 1.009],
                ]
            )
            * 1e-4
        )

        assert_almost_equal(mse2, self.res.forecast_cov(3)[1], DECIMAL_3)

    def test_irf_stderr(self):
        irf_stderr = self.irf.stderr(orth=False)
        for i in range(1, 1 + len(self.lut.irf_stderr)):
            assert_almost_equal(
                np.round(irf_stderr[i], 3), self.lut.irf_stderr[i - 1]
            )

    def test_cum_irf_stderr(self):
        stderr = self.irf.cum_effect_stderr(orth=False)
        for i in range(1, 1 + len(self.lut.cum_irf_stderr)):
            assert_almost_equal(
                np.round(stderr[i], 3), self.lut.cum_irf_stderr[i - 1]
            )

    def test_lr_effect_stderr(self):
        stderr = self.irf.lr_effect_stderr(orth=False)
        orth_stderr = self.irf.lr_effect_stderr(orth=True)
        assert_almost_equal(np.round(stderr, 3), self.lut.lr_stderr)


def test_get_trendorder():
    results = {"c": 1, "n": 0, "ct": 2, "ctt": 3}

    for t, trendorder in results.items():
        assert util.get_trendorder(t) == trendorder


def test_var_constant():
    # see 2043
    import datetime

    from pandas import DataFrame, DatetimeIndex

    series = np.array([[2.0, 2.0], [1, 2.0], [1, 2.0], [1, 2.0], [1.0, 2.0]])
    data = DataFrame(series)

    d = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    index = []
    for i in range(data.shape[0]):
        index.append(d)
        d += delta

    data.index = DatetimeIndex(index)

    # with pytest.warns(ValueWarning):  #does not silence warning in test output
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=ValueWarning)
        model = VAR(data)
    with pytest.raises(ValueError):
        model.fit(1)


def test_var_trend():
    # see 2271
    data = get_macrodata().view((float, 3), type=np.ndarray)

    model = VAR(data)
    results = model.fit(4)  # , trend = 'c')
    irf = results.irf(10)

    data_nc = data - data.mean(0)
    model_nc = VAR(data_nc)
    results_nc = model_nc.fit(4, trend="n")
    with pytest.raises(ValueError):
        model.fit(4, trend="t")


def test_irf_trend():
    # test for irf with different trend see #1636
    # this is a rough comparison by adding trend or subtracting mean to data
    # to get similar AR coefficients and IRF
    data = get_macrodata().view((float, 3), type=np.ndarray)

    model = VAR(data)
    results = model.fit(4)  # , trend = 'c')
    irf = results.irf(10)

    data_nc = data - data.mean(0)
    model_nc = VAR(data_nc)
    results_nc = model_nc.fit(4, trend="n")
    irf_nc = results_nc.irf(10)

    assert_allclose(irf_nc.stderr()[1:4], irf.stderr()[1:4], rtol=0.01)

    trend = 1e-3 * np.arange(len(data)) / (len(data) - 1)
    # for pandas version, currently not used, if data is a pd.DataFrame
    # data_t = pd.DataFrame(data.values + trend[:,None], index=data.index, columns=data.columns)
    data_t = data + trend[:, None]

    model_t = VAR(data_t)
    results_t = model_t.fit(4, trend="ct")
    irf_t = results_t.irf(10)

    assert_allclose(irf_t.stderr()[1:4], irf.stderr()[1:4], rtol=0.03)


class TestVARExtras(object):
    @classmethod
    def setup_class(cls):
        mdata = macrodata.load_pandas().data
        mdata = mdata[["realgdp", "realcons", "realinv"]]
        data = mdata.values
        data = np.diff(np.log(data), axis=0) * 400
        cls.res0 = VAR(data).fit(maxlags=2)

    def test_process(self, close_figures):
        res0 = self.res0
        k_ar = res0.k_ar
        fc20 = res0.forecast(res0.endog[-k_ar:], 20)
        mean_lr = res0.mean()
        assert_allclose(mean_lr, fc20[-1], rtol=5e-4)

        ysim = res0.simulate_var(seed=987128)
        assert_allclose(ysim.mean(0), mean_lr, rtol=0.1)
        # initialization does not use long run intercept, see #4542
        assert_allclose(ysim[0], res0.intercept, rtol=1e-10)
        assert_allclose(ysim[1], res0.intercept, rtol=1e-10)

        n_sim = 900
        ysimz = res0.simulate_var(
            steps=n_sim, offset=np.zeros((n_sim, 3)), seed=987128
        )
        zero3 = np.zeros(3)
        assert_allclose(ysimz.mean(0), zero3, atol=0.4)
        # initialization does not use long run intercept, see #4542
        assert_allclose(ysimz[0], zero3, atol=1e-10)
        assert_allclose(ysimz[1], zero3, atol=1e-10)

        # check attributes
        assert_equal(res0.k_trend, 1)
        assert_equal(res0.k_exog_user, 0)
        assert_equal(res0.k_exog, 1)
        assert_equal(res0.k_ar, 2)

        irf = res0.irf()

    @pytest.mark.matplotlib
    def test_process_plotting(self, close_figures):
        # Partially a smoke test
        res0 = self.res0
        k_ar = res0.k_ar
        fc20 = res0.forecast(res0.endog[-k_ar:], 20)
        irf = res0.irf()

        res0.plotsim()
        res0.plot_acorr()

        fig = res0.plot_forecast(20)
        fcp = fig.axes[0].get_children()[1].get_ydata()[-20:]
        # Note values are equal, but keep rtol buffer
        assert_allclose(fc20[:, 0], fcp, rtol=1e-13)
        fcp = fig.axes[1].get_children()[1].get_ydata()[-20:]
        assert_allclose(fc20[:, 1], fcp, rtol=1e-13)
        fcp = fig.axes[2].get_children()[1].get_ydata()[-20:]
        assert_allclose(fc20[:, 2], fcp, rtol=1e-13)

        fig_asym = irf.plot()
        fig_mc = irf.plot(stderr_type="mc", repl=1000, seed=987128)

        for k in range(3):
            a = fig_asym.axes[1].get_children()[k].get_ydata()
            m = fig_mc.axes[1].get_children()[k].get_ydata()
            # use m as desired because it is larger
            # a is for some irf much smaller than m
            assert_allclose(a, m, atol=0.1, rtol=0.9)

    def test_forecast_cov(self):
        # forecast_cov can include parameter uncertainty if contant-only
        res = self.res0

        covfc1 = res.forecast_cov(3)
        assert_allclose(covfc1, res.mse(3), rtol=1e-13)
        # ignore warning, TODO: assert OutputWarning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            covfc2 = res.forecast_cov(3, method="auto")
        assert_allclose(covfc2, covfc1, rtol=0.05)
        # regression test, TODO: replace with verified numbers (Stata)
        res_covfc2 = np.array(
            [
                [
                    [9.45802013, 4.94142038, 37.1999646],
                    [4.94142038, 7.09273624, 5.66215089],
                    [37.1999646, 5.66215089, 259.61275869],
                ],
                [
                    [11.30364479, 5.72569141, 49.28744123],
                    [5.72569141, 7.409761, 10.98164091],
                    [49.28744123, 10.98164091, 336.4484723],
                ],
                [
                    [12.36188803, 6.44426905, 53.54588026],
                    [6.44426905, 7.88850029, 13.96382545],
                    [53.54588026, 13.96382545, 352.19564327],
                ],
            ]
        )
        assert_allclose(covfc2, res_covfc2, atol=1e-6)

    def test_exog(self):
        # check that trend and exog are equivalent for basics and varsim
        data = self.res0.model.endog
        res_lin_trend = VAR(data).fit(maxlags=2, trend="ct")
        ex = np.arange(len(data))
        res_lin_trend1 = VAR(data, exog=ex).fit(maxlags=2)
        ex2 = np.arange(len(data))[:, None] ** [0, 1]
        res_lin_trend2 = VAR(data, exog=ex2).fit(maxlags=2, trend="n")
        # TODO: intercept differs by 4e-3, others are < 1e-12
        assert_allclose(res_lin_trend.params, res_lin_trend1.params, rtol=5e-3)
        assert_allclose(res_lin_trend.params, res_lin_trend2.params, rtol=5e-3)
        assert_allclose(
            res_lin_trend1.params, res_lin_trend2.params, rtol=1e-10
        )

        y1 = res_lin_trend.simulate_var(seed=987128)
        y2 = res_lin_trend1.simulate_var(seed=987128)
        y3 = res_lin_trend2.simulate_var(seed=987128)
        assert_allclose(y2.mean(0), y1.mean(0), rtol=1e-12)
        assert_allclose(y3.mean(0), y1.mean(0), rtol=1e-12)
        assert_allclose(y3.mean(0), y2.mean(0), rtol=1e-12)

        h = 10
        fc1 = res_lin_trend.forecast(res_lin_trend.endog[-2:], h)
        exf = np.arange(len(data), len(data) + h)
        fc2 = res_lin_trend1.forecast(
            res_lin_trend1.endog[-2:], h, exog_future=exf
        )
        with pytest.raises(ValueError, match="exog_future only has"):
            wrong_exf = np.arange(len(data), len(data) + h // 2)
            res_lin_trend1.forecast(
                res_lin_trend1.endog[-2:], h, exog_future=wrong_exf
            )
        exf2 = exf[:, None] ** [0, 1]
        fc3 = res_lin_trend2.forecast(
            res_lin_trend2.endog[-2:], h, exog_future=exf2
        )
        assert_allclose(fc2, fc1, rtol=1e-12)
        assert_allclose(fc3, fc1, rtol=1e-12)
        assert_allclose(fc3, fc2, rtol=1e-12)

        fci1 = res_lin_trend.forecast_interval(res_lin_trend.endog[-2:], h)
        exf = np.arange(len(data), len(data) + h)
        fci2 = res_lin_trend1.forecast_interval(
            res_lin_trend1.endog[-2:], h, exog_future=exf
        )
        exf2 = exf[:, None] ** [0, 1]
        fci3 = res_lin_trend2.forecast_interval(
            res_lin_trend2.endog[-2:], h, exog_future=exf2
        )
        assert_allclose(fci2, fci1, rtol=1e-12)
        assert_allclose(fci3, fci1, rtol=1e-12)
        assert_allclose(fci3, fci2, rtol=1e-12)


def test_var_cov_params_pandas(bivariate_var_data):
    df = pd.DataFrame(bivariate_var_data, columns=["x", "y"])
    mod = VAR(df)
    res = mod.fit(2)
    cov = res.cov_params()
    assert isinstance(cov, pd.DataFrame)
    exog_names = ("const", "L1.x", "L1.y", "L2.x", "L2.y")
    index = pd.MultiIndex.from_product((exog_names, ("x", "y")))
    assert_index_equal(cov.index, cov.columns)
    assert_index_equal(cov.index, index)


def test_summaries_exog(reset_randomstate):
    y = np.random.standard_normal((500, 6))
    df = pd.DataFrame(y)
    cols = ["endog_{0}".format(i) for i in range(2)] + [
        "exog_{0}".format(i) for i in range(4)
    ]
    df.columns = cols
    df.index = pd.date_range("1-1-1950", periods=500, freq="MS")
    endog = df.iloc[:, :2]
    exog = df.iloc[:, 2:]

    res = VAR(endog=endog, exog=exog).fit(maxlags=0)
    summ = res.summary().summary
    assert "exog_0" in summ
    assert "exog_1" in summ
    assert "exog_2" in summ
    assert "exog_3" in summ

    res = VAR(endog=endog, exog=exog).fit(maxlags=2)
    summ = res.summary().summary
    assert "exog_0" in summ
    assert "exog_1" in summ
    assert "exog_2" in summ
    assert "exog_3" in summ


def test_whiteness_nlag(reset_randomstate):
    # GH 6686
    y = np.random.standard_normal((200, 2))
    res = VAR(y).fit(maxlags=1, ic=None)
    with pytest.raises(ValueError, match="The whiteness test can only"):
        res.test_whiteness(1)


def test_var_maxlag(reset_randomstate):
    y = np.random.standard_normal((22, 10))
    VAR(y).fit(maxlags=None, ic="aic")
    with pytest.raises(ValueError, match="maxlags is too large"):
        VAR(y).fit(maxlags=8, ic="aic")


def test_from_formula():
    with pytest.raises(NotImplementedError):
        VAR.from_formula("y ~ x", None)


def test_correct_nobs():
    # GH6748
    mdata = macrodata.load_pandas().data
    # prepare the dates index
    dates = mdata[["year", "quarter"]].astype(int).astype(str)
    quarterly = dates["year"] + "Q" + dates["quarter"]
    quarterly = dates_from_str(quarterly)
    mdata = mdata[["realgdp", "realcons", "realinv"]]
    mdata.index = pd.DatetimeIndex(quarterly)
    data = np.log(mdata).diff().dropna()
    data.index.freq = data.index.inferred_freq
    data_exog = pd.DataFrame(index=data.index)
    data_exog["exovar1"] = np.random.normal(size=data_exog.shape[0])
    # make a VAR model
    model = VAR(endog=data, exog=data_exog)
    results = model.fit(maxlags=1)
    irf = results.irf_resim(
        orth=False, repl=100, steps=10, seed=1, burn=100, cum=False
    )
    assert irf.shape == (100, 11, 3, 3)


@pytest.mark.slow
def test_irf_err_bands():
    # smoke tests
    data = get_macrodata()
    model = VAR(data)
    results = model.fit(maxlags=2)
    irf = results.irf()
    bands_sz1 = irf.err_band_sz1()
    bands_sz2 = irf.err_band_sz2()
    bands_sz3 = irf.err_band_sz3()
    bands_mc = irf.errband_mc()
