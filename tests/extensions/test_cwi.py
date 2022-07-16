import pandas as pd
import numpy as np
from datetime import datetime
from ..test_utils import TestUtlis as tu
import pytest
from pyinvestingsnippets.exceptions.cwi_not_properly_called_exception import CwiNotProperlyCalledException


def test_no_return_object_passed():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    with pytest.raises(CwiNotProperlyCalledException):
        returns.cwi


def test_caller():
    prices = tu.gbm(10, 1, steps_per_year=252)
    assert prices.returns.cwi is not None
    assert prices.log_returns.cwi is not None


def test_cwi():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    prices = pd.Series(data=[10, 14, 18.2, 21.84, 32.76], index=index_range)
    assert prices.returns.cwi is not None
    assert isinstance(prices.returns.cwi.data, pd.Series)
    assert prices.returns.cwi.data.dtypes == 'float64'
    assert prices.returns.cwi.data['2000-01-01'] == 1
    np.testing.assert_almost_equal(prices.returns.cwi.data['2001-01-01'], 1.4)
    np.testing.assert_almost_equal(prices.returns.cwi.data['2002-01-01'], 1.82)
    np.testing.assert_almost_equal(prices.returns.cwi.data['2003-01-01'], 2.184)
    np.testing.assert_almost_equal(prices.returns.cwi.data['2004-01-01'], 3.276)


def test_get_total_return():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    prices = pd.Series(data=[10, 14, 18.2, 21.84, 32.76], index=index_range)
    np.testing.assert_almost_equal(prices.returns.cwi.total_return, 2.276)
