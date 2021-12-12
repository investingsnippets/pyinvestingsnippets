import pandas as pd
import numpy as np
from datetime import datetime
from scipy.stats import truncnorm
import pytest

import pyinvestingsnippets as pyinv

from ..test_utils import TestUtlis as tu


def test_rolling_volatility_monthly():
    number_of_values = 30*3
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=number_of_values, freq='D')
    values = tu.get_truncated_normal(mean=0, sd=2, low=-0.90, upp=0.90)
    returns = pd.Series(data=values.rvs(number_of_values), index=index_range)
    rolling_rets = pyinv.RollingVolatility(returns, rolling_window=10, window=252)
    rolling_rets_df = rolling_rets.data
    assert rolling_rets_df is not None
    assert isinstance(rolling_rets_df, pd.Series)
    assert rolling_rets_df.dtypes == 'float64'
    assert rolling_rets_df.name == 'Rolling_Vol'
    assert rolling_rets_df[1:9].isna().all()


def test_rolling_volatility_negative_windows():
    number_of_values = 30*3
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=number_of_values, freq='D')
    values = tu.get_truncated_normal(mean=0, sd=2, low=-0.90, upp=0.90)
    returns = pd.Series(data=values.rvs(number_of_values), index=index_range)
    with pytest.raises(AssertionError) as excinfo:
        pyinv.RollingVolatility(returns, rolling_window=-2, window=252)
    assert "rolling_window must be possitive integer" in str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        pyinv.RollingVolatility(returns, rolling_window=1, window=-1)
    assert "window must be possitive integer" in str(excinfo.value)


def test_rolling_volatility_non_int_windows():
    number_of_values = 30*3
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=number_of_values, freq='D')
    values = tu.get_truncated_normal(mean=0, sd=2, low=-0.90, upp=0.90)
    returns = pd.Series(data=values.rvs(number_of_values), index=index_range)
    with pytest.raises(AssertionError) as excinfo:
        pyinv.RollingVolatility(returns, rolling_window=1.3, window=252)
    assert "rolling_window must be possitive integer" in str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        pyinv.RollingVolatility(returns, rolling_window=1, window=1.3)
    assert "window must be possitive integer" in str(excinfo.value)
