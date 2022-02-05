import pandas as pd
import numpy as np
from datetime import datetime

from ..test_utils import TestUtlis as tu


def test_cumulative_return():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='D')
    prices = pd.Series(data=[100, 90, 113, 120, 130], index=index_range)
    assert round(prices.prices.cumulative_return, 2) == 0.30
