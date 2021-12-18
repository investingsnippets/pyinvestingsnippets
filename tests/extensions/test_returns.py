import pandas as pd
import numpy as np
from datetime import datetime

from ..test_utils import TestUtlis as tu

def test_annualized():
    # generate some returns
    number_of_values = 252*2
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=number_of_values, freq='D')
    values = tu.get_truncated_normal(mean=0.001, sd=2, low=-0.01, upp=0.01)
    returns = pd.Series(data=values.rvs(number_of_values), index=index_range)
    # We do a trick here where from a plain object filled with returns
    # we construct a ealth index which simulates prices :)
    prices = returns.wealth_index.data
    annualized_rets = prices.returns.annualized(252)
    assert annualized_rets is not None
    assert isinstance(annualized_rets, float)

    annualized_vol = prices.returns.volatility_annualized(252)
    assert annualized_vol is not None
    assert isinstance(annualized_vol, float)
