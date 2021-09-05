import pandas as pd
import numpy as np
from pyinvestingsnippets import WealthIndex


def test_wealth_index():
    index_range = pd.date_range(start=pd.datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    wi = WealthIndex(returns)
    assert wi is not None
    wi_index = wi.get_wealth_index()
    assert wi_index is not None
    assert isinstance(wi_index, pd.Series)
    assert wi_index.dtypes == 'float64'
    assert wi_index.name == 'WealthIndex'
    print(wi_index)
    assert pd.isnull(wi_index['2000-01-01'])
    np.testing.assert_almost_equal(wi_index['2001-01-01'], 1.4)
    np.testing.assert_almost_equal(wi_index['2002-01-01'], 1.82)
    np.testing.assert_almost_equal(wi_index['2003-01-01'], 2.184)
    np.testing.assert_almost_equal(wi_index['2004-01-01'], 3.276)


def test_get_total_return():
    index_range = pd.date_range(start=pd.datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    wi = WealthIndex(returns)
    wi_total_ret = wi.get_total_return()
    np.testing.assert_almost_equal(wi_total_ret, 3.276)

def test_get_compound_annual_growth_rate():
    index_range = pd.date_range(start=pd.datetime(2000, 1, 1), periods=5, freq='AS-JAN')
    returns = pd.Series(data=[np.nan, 0.4, 0.3, 0.2, 0.5], index=index_range)
    wi = WealthIndex(returns)
    wi_total_ret = wi.get_compound_annual_growth_rate()
    np.testing.assert_almost_equal(wi_total_ret, 0.2678526)

