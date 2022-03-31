import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ..test_utils import TestUtlis as tu

def test_returns():
    # generate some returns
    prices = tu.gbm(10, 1, steps_per_year=252)
    # From prices we now get the returns
    assert prices.annual_returns is not None
    # Make sure that the first value is always NaN
    assert np.isnan(prices.annual_returns.head(1).values[0])
    some_date_soon = datetime.now() - timedelta(days=5*252)
    assert prices.annual_returns[some_date_soon.year:].all() == prices.annual_returns.data[some_date_soon.year:].all()
    assert prices.annual_returns().all() == prices.annual_returns.data.all()

def test_annualized():
    prices = tu.gbm(10, 1, steps_per_year=252)
    annualized_rets = prices.annual_returns.annualized
    assert annualized_rets is not None
    assert isinstance(annualized_rets, float)

    annualized_vol = prices.annual_returns.volatility_annualized
    assert annualized_vol is not None
    assert isinstance(annualized_vol, float)

def test_var():
    prices = tu.gbm(10, 1, steps_per_year=252)
    var = prices.annual_returns.var()
    assert not np.isnan(var)
    cvar = prices.annual_returns.cvar()
    assert not np.isnan(cvar)
