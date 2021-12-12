import pandas as pd
import numpy as np
from datetime import datetime

from ..test_utils import TestUtlis as tu

def test_price():
    # generate some prices
    number_of_values = 252*2
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=number_of_values, freq='D')
    values = tu.get_truncated_normal(mean=0.001, sd=2, low=-0.01, upp=0.01)
    returns = pd.Series(data=values.rvs(number_of_values), index=index_range)
    prices = returns.wealth_index.data
    assert prices is not None
    assert isinstance(prices, pd.Series)
    assert prices.dtypes == 'float64'
    assert prices.returns is not None
    assert returns['2000-01-03':].all() == prices.returns.data['2000-01-03':].all()
