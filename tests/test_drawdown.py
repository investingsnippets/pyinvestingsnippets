import pandas as pd
from pyinvestingsnippets import Drawdown


def test_drawdown():
    wealth_index = pd.DataFrame()
    dd = Drawdown(wealth_index)
    assert dd is not None