# pylint: disable=E501
# flake8: noqa
"""Python tools for stock analysis"""
from .extensions.drawdown import Drawdown
from .extensions.cumulative_wealth_index import CumulativeWealthIndex
from .extensions.monthly_returns import MonthlyReturns
from .extensions.annual_returns import AnnualReturns
from .extensions.weekly_returns import WeeklyReturns
from .extensions.prices import Prices
from .extensions.returns import Returns
from .extensions.log_returns import LogReturns
from .extensions.srri import SRRI

from .utilities.rolling_returns import RollingReturns
from .utilities.rolling_volatility import RollingVolatility
from .utilities.rolling_beta_regression import RollingBetaRegression
from .utilities.rolling_beta_covariance import RollingBetaCovariance
from .utilities.exponentially_weighted_downside_risk import (
    ExponantiallyWeightedDownsideRisk,
)
from .utilities.beta_covariance import BetaCovariance
from .utilities.beta_regression import BetaRegression


__version__ = "2.0.0"
__all__ = [
    "Drawdown",
    "CumulativeWealthIndex",
    "Prices",
    "SRRI",
    "MonthlyReturns",
    "WeeklyReturns",
    "AnnualReturns",
    "Returns",
    "LogReturns",
    "RollingReturns",
    "RollingVolatility",
    "BetaCovariance",
    "BetaRegression",
    "ExponantiallyWeightedDownsideRisk",
    "RollingBetaRegression",
    "RollingBetaCovariance",
]
