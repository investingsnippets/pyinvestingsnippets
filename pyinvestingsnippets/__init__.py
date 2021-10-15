# pylint: disable=E501
# flake8: noqa
"""Python tools for stock analysis"""
from .extensions.drawdown import Drawdown
from .extensions.wealthindex import WealthIndex
from .extensions.monthly_returns import MonthlyReturns
from .extensions.annual_returns import AnnualReturns
from .extensions.weekly_returns import WeeklyReturns
from .extensions.prices import Prices
from .extensions.returns import Returns
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


__version__ = "1.0.1"
__all__ = [
    "Drawdown",
    "WealthIndex",
    "Prices",
    "SRRI",
    "MonthlyReturns",
    "WeeklyReturns",
    "AnnualReturns",
    "Returns",
    "RollingReturns",
    "RollingVolatility",
    "BetaCovariance",
    "BetaRegression",
    "ExponantiallyWeightedDownsideRisk",
    "RollingBetaRegression",
    "RollingBetaCovariance",
]
