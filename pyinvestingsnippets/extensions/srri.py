import pandas as pd
import numpy as np


@pd.api.extensions.register_series_accessor("srri")
class SRRI:
    """
    Synthetic Risk and Reward Indicator (Standard Deviation over 5 Years)
    https://www.esma.europa.eu/sites/default/files/library/2015/11/10_673.pdf

    The volatility of the fund shall be computed,
    and then rescaled to a yearly basis, using the
    following standard method:
    volatility = sigma_{f} = \\sqrt( (m/T-1) * \\sum{t=1}{T}(r_f,t - r-mean_f)**2 )
    where the returns of the fund are measured over T
    non overlapping periods of the duration of 1/m years.
    This means m=52 and T= 260 for weekly returns, and m=12 and T=60 for monthly
    returns; and where r-mean_f is the arithmetic mean of
    the returns of the fund over the T periods
    """

    RISK_CLASSES = {
        1: {"low": 0, "high": 0.005},
        2: {"low": 0.005, "high": 0.02},
        3: {"low": 0.02, "high": 0.05},
        4: {"low": 0.05, "high": 0.1},
        5: {"low": 0.1, "high": 0.15},
        6: {"low": 0.15, "high": 0.25},
        7: {"low": 0.25, "high": 1},
    }

    def __init__(self, pandas_obj) -> None:
        pandas_obj = pandas_obj.dropna()
        self._validate(pandas_obj)
        deviations = pandas_obj - pandas_obj.mean()
        squared_deviations = np.sum(deviations ** 2)
        factor = 52 / (260 - 1) if pandas_obj.shape[0] == 260 else 12 / (60 - 1)
        to_root = factor * squared_deviations
        self._obj = np.sqrt(to_root)

    @staticmethod
    def _validate(obj):
        # 5 years of weekly returns data (5 * 52) or 5 * 12 monthly
        assert obj.shape[0] in [260, 60]

    @property
    def value(self):
        return self._obj

    @property
    def risk_class(self):
        for i in SRRI.RISK_CLASSES:
            if (
                self._obj >= SRRI.RISK_CLASSES[i]["low"]
                and self._obj < SRRI.RISK_CLASSES[i]["high"]
            ):
                return i
