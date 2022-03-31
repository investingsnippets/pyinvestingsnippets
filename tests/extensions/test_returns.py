import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ..test_utils import TestUtlis as tu

def test_returns():
    # generate some returns
    prices = tu.gbm(10, 1, steps_per_year=252)
    # From prices we now get the returns
    assert prices.returns is not None
    # Make sure that the first value is always NaN
    assert np.isnan(prices.returns.head(1).values[0])
    some_date_soon = datetime.now() - timedelta(days=5*252)
    assert prices.returns[some_date_soon:].all() == prices.returns.data[some_date_soon:].all()
    assert prices.returns().all() == prices.returns.data.all()

def test_annualized():
    prices = tu.gbm(10, 1, steps_per_year=252)
    annualized_rets = prices.returns.annualized(252)
    assert annualized_rets is not None
    assert isinstance(annualized_rets, float)

    annualized_vol = prices.returns.volatility_annualized(252)
    assert annualized_vol is not None
    assert isinstance(annualized_vol, float)

def test_var():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='D')
    prices = pd.Series(data=[100, 90, 113, 120, 130], index=index_range)
    var = prices.returns.var()
    assert not np.isnan(var)
    np.testing.assert_almost_equal(var, 0.0757079)
    cvar = prices.returns.cvar()
    assert not np.isnan(cvar)
    np.testing.assert_almost_equal(cvar, 0.0999999)

def test_total_return():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='D')
    prices = pd.Series(data=[100, 90, 113, 120, 130], index=index_range)
    assert round(prices.returns.total, 2) == 0.30

def test_sharpe():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='D')
    prices = pd.Series(data=[100, 90, 113, 120, 130], index=index_range)
    assert round(prices.returns.sharpe(0.2, periods=5), 2) == 0.39
