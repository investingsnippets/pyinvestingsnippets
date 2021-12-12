import pandas as pd
import numpy as np
from datetime import datetime


def test_wealth_index():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    assert returns.wealth_index is not None
    assert isinstance(returns.wealth_index.data, pd.Series)
    assert returns.wealth_index.data.dtypes == 'float64'
    assert returns.wealth_index.data['2000-01-01'] == 1
    np.testing.assert_almost_equal(returns.wealth_index.data['2001-01-01'], 1.4)
    np.testing.assert_almost_equal(returns.wealth_index.data['2002-01-01'], 1.82)
    np.testing.assert_almost_equal(returns.wealth_index.data['2003-01-01'], 2.184)
    np.testing.assert_almost_equal(returns.wealth_index.data['2004-01-01'], 3.276)

def test_get_total_return():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    np.testing.assert_almost_equal(returns.wealth_index.total_return, 2.276)

def test_get_compound_annual_growth_rate():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    np.testing.assert_almost_equal(returns.wealth_index.cagr, 0.2678526)

