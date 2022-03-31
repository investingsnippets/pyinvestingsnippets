import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ..test_utils import TestUtlis as tu

def test_returns():
    # generate some returns
    prices = tu.gbm(10, 1, steps_per_year=252)
    # From prices we now get the returns
    assert prices.monthly_returns is not None
    # Make sure that the first value is always NaN
    assert np.isnan(prices.monthly_returns.head(1).values[0])
    some_date_soon = datetime.now() - timedelta(days=5*252)
    assert prices.monthly_returns[some_date_soon:].all() == prices.monthly_returns.data[some_date_soon:].all()
    assert prices.monthly_returns().all() == prices.monthly_returns.data.all()

def test_annualized():
    prices = tu.gbm(10, 1, steps_per_year=252)
    annualized_rets = prices.monthly_returns.annualized
    assert annualized_rets is not None
    assert isinstance(annualized_rets, float)

    annualized_vol = prices.monthly_returns.volatility_annualized
    assert annualized_vol is not None
    assert isinstance(annualized_vol, float)

def test_var():
    prices = tu.gbm(10, 1, steps_per_year=252)
    var = prices.monthly_returns.var()
    assert not np.isnan(var)
    cvar = prices.monthly_returns.cvar()
    assert not np.isnan(cvar)