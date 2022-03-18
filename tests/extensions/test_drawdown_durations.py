import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def test_durations():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=9, freq='AS-JAN')
    cwi = pd.Series(data=[0.4, 0.3, 0.2, 0.5, 0.4, 0.4, 0.3, 0.3, 0.5], index=index_range) 
    durations = cwi.drawdown.durations
    assert len(durations.data) == 2
    assert durations['2003-01-01'] == timedelta(days=1096)
    assert durations['2008-01-01'] == timedelta(days=1826)
    assert durations.mean == timedelta(days=1461)
    assert durations.max == timedelta(1826)


def test_durations_empty_drawdown():
    index_range = pd.date_range(start=datetime(2000, 1, 1), periods=9, freq='AS-JAN')
    cwi = pd.Series(data=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], index=index_range) 
    durations = cwi.drawdown.durations
    assert len(durations.data) == 0
    assert durations.mean == timedelta(days=0)
    assert durations.max == timedelta(0)