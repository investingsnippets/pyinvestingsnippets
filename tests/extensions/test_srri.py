import pandas as pd
import numpy as np
from datetime import datetime
from ..test_utils import TestUtlis as tu

from pyinvestingsnippets import SRRI


def test_srri_on_weekly():
    number_of_values = 52*5
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=number_of_values, freq='W')
    values = tu.get_truncated_normal(mean=0.001, sd=2, low=-0.30, upp=0.30)
    returns = pd.Series(data=values.rvs(number_of_values), index=index_range)
    srri = SRRI(returns)
    assert srri is not None
    assert srri.value > 1
    assert srri.risk_class == 7

    values = tu.get_truncated_normal(mean=0.001, sd=2, low=-0.10, upp=0.10)
    returns = pd.Series(data=values.rvs(number_of_values), index=index_range)
    srri = SRRI(returns)
    assert srri is not None
    assert srri.value < 1
    assert srri.risk_class == 7

    values = tu.get_truncated_normal(mean=0.001, sd=2, low=-0.01, upp=0.01)
    returns = pd.Series(data=values.rvs(number_of_values), index=index_range)
    srri = SRRI(returns)
    assert srri is not None
    assert srri.value < 1
    assert srri.risk_class == 3


def test_srri_on_monthly():
    number_of_values = 12*5
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=number_of_values, freq='W')
    values = tu.get_truncated_normal(mean=0.001, sd=2, low=-0.015, upp=0.015)
    returns = pd.Series(data=values.rvs(number_of_values), index=index_range)
    srri = SRRI(returns)
    assert srri is not None
    assert srri.value < 1
    assert srri.risk_class == 3
