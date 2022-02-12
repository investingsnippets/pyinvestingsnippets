import pandas as pd
import numpy as np
from datetime import datetime


def test_cwi():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    assert returns.cwi is not None
    assert isinstance(returns.cwi.data, pd.Series)
    assert returns.cwi.data.dtypes == 'float64'
    assert returns.cwi.data['2000-01-01'] == 1
    np.testing.assert_almost_equal(returns.cwi.data['2001-01-01'], 1.4)
    np.testing.assert_almost_equal(returns.cwi.data['2002-01-01'], 1.82)
    np.testing.assert_almost_equal(returns.cwi.data['2003-01-01'], 2.184)
    np.testing.assert_almost_equal(returns.cwi.data['2004-01-01'], 3.276)

def test_get_total_return():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    np.testing.assert_almost_equal(returns.cwi.total_return, 2.276)
