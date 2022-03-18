import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def test_drawdown_and_returns_series():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=4, freq='AS-JAN')
    cwi = pd.Series(data=[0.4, 0.3, 0.2, 0.5], index=index_range)
    dd = cwi.drawdown
    assert dd is not None
    drawdown_df = dd.data
    assert drawdown_df is not None
    assert isinstance(drawdown_df, pd.Series)
    assert drawdown_df.dtypes == 'float64'
    assert drawdown_df.name == cwi.name
    np.testing.assert_almost_equal(drawdown_df['2000-01-01'], 0.0)
    np.testing.assert_almost_equal(drawdown_df['2001-01-01'], -0.25)
    np.testing.assert_almost_equal(drawdown_df['2002-01-01'], -0.5)
    np.testing.assert_almost_equal(drawdown_df['2003-01-01'], 0.0)


def test_max_drawdown():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=4, freq='AS-JAN')
    cwi = pd.Series(data=[0.4, 0.3, 0.2, 0.5], index=index_range)
    assert cwi.drawdown.max_drawdown == -0.5

