import pandas as pd
import numpy as np
import pyinvestingsnippets
from datetime import datetime


def test_price():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    data = pd.Series(data=[120.0, 124, 139.3, 120, 100], index=index_range)
    assert data.prices is not None
    assert isinstance(data.prices.data, pd.Series)
    assert data.prices.data.dtypes == 'float64'
    assert data.prices.data['2000-01-01'] == 120

    print(data.prices.returns.wealth_index_since(since='2002-01-01').data)
