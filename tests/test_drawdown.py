import pandas as pd
import numpy as np
from pyinvestingsnippets import Drawdown


def test_drawdown_and_returns_series():
    wealth_index = pd.Series(data=[0.4, 0.3, 0.2, 0.5], index=[0,1,2,3])
    dd = Drawdown(wealth_index)
    assert dd is not None
    drawdown_df = dd.get_drawdown()
    assert drawdown_df is not None
    assert isinstance(drawdown_df, pd.Series)
    assert drawdown_df.dtypes == 'float64'
    assert drawdown_df.name == 'Drawdown'
    np.testing.assert_almost_equal(drawdown_df[0], 0.0)
    np.testing.assert_almost_equal(drawdown_df[1], -0.25)
    np.testing.assert_almost_equal(drawdown_df[2], -0.5)
    np.testing.assert_almost_equal(drawdown_df[3], 0.0)


def test_max_drawdown():
    wealth_index = pd.Series(data=[0.4, 0.3, 0.2, 0.5], index=[0,1,2,3])
    dd = Drawdown(wealth_index)
    assert dd.get_max_drawdown() == -0.5


def test_durations():
    wealth_index = pd.Series(data=[0.4, 0.3, 0.2, 0.5, 0.4, 0.4, 0.3, 0.3, 0.5], index=[0,1,2,3,4,5,6,7,8]) 
    dd = Drawdown(wealth_index)
    durations = dd.compute_drawdown_lagoons_durations()
    assert isinstance(durations, pd.Series)
    assert durations.dtypes == 'float64'
    assert durations.name == 'Durations'
    assert len(durations) == 2
    assert durations[3] == 3
    assert durations[8] == 5
