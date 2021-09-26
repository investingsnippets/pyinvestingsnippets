import pandas as pd
import numpy as np
import pyinvestingsnippets
from datetime import datetime


def test_price():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='W-SUN')
    data = pd.Series(data=[100, 96, 89+5, 86, 90], index=index_range)
    assert data.prices is not None
    pandas_obj = data.prices.data.pct_change()
    deviations = pandas_obj - pandas_obj.mean()
    squared_deviations = np.sum(deviations**2)
    to_root = (52/(260-1)) * squared_deviations
    print(np.sqrt(to_root))
