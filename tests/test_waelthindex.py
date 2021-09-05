import pandas as pd
import numpy as np
from pyinvestingsnippets import WealthIndex


def test_wealth_index():
    index_range = pd.date_range(start=pd.datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    assert returns.WealthIndex is not None
    assert isinstance(returns.WealthIndex.wealth_index, pd.Series)
    assert returns.WealthIndex.wealth_index.dtypes == 'float64'
    assert returns.WealthIndex.wealth_index.name == 'WealthIndex'
    assert returns.WealthIndex.wealth_index['2000-01-01'] == 1
    np.testing.assert_almost_equal(returns.WealthIndex.wealth_index['2001-01-01'], 1.4)
    np.testing.assert_almost_equal(returns.WealthIndex.wealth_index['2002-01-01'], 1.82)
    np.testing.assert_almost_equal(returns.WealthIndex.wealth_index['2003-01-01'], 2.184)
    np.testing.assert_almost_equal(returns.WealthIndex.wealth_index['2004-01-01'], 3.276)

def test_get_total_return():
    index_range = pd.date_range(start=pd.datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    np.testing.assert_almost_equal(returns.WealthIndex.total_return, 3.276)

def test_get_compound_annual_growth_rate():
    index_range = pd.date_range(start=pd.datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    np.testing.assert_almost_equal(returns.WealthIndex.cagr, 0.2678526)

