import pandas as pd
import numpy as np
from datetime import datetime

from ..test_utils import TestUtlis as tu

def test_returns():
    # generate some returns
    prices = tu.gbm(10, 1, steps_per_year=252)
    # From prices we now get the returns
    assert prices.returns is not None
    assert prices.returns['2000-01-03':].all() == prices.returns.data['2000-01-03':].all()
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
    prices = tu.gbm(10, 1, steps_per_year=252)
    var = prices.returns.var()
    cvar = prices.returns.cvar()

def test_total_return():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='D')
    prices = pd.Series(data=[100, 90, 113, 120, 130], index=index_range)
    assert round(prices.returns.total, 2) == 0.30
