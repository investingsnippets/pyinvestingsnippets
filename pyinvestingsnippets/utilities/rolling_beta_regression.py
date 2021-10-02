import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression


class RollingBetaRegression:
    """
    Given a Returns Series calculates the beta.

    Beta: y = a + (b*x): A way to calculate beta is to use a linear
    regression formula. Where beta is the coefficient of the independent
    variable (x in the equation), y is the dependent variable,
    a is the y-intercept or constant, and b is the slope of the line.

    We use the lenear regression formula in this implementation.
    """

    def __init__(self, independent_variable, dependent_variable, window):
        """
        Calculates the rolling beta of a Stock over the
        Benchmark index using linear regression

        Parameters
        ----------
        independent_variable : Market Returns
        dependent_variable : Stock Returns
        window : rolling window
        """

        self.independent_variable = independent_variable.dropna()
        self.dependent_variable = dependent_variable.dropna()
        self.window = window

        obs = len(self.independent_variable)
        betas = np.full(obs, np.nan)
        alphas = np.full(obs, np.nan)

        for i in range((obs - window)):
            model = LinearRegression().fit(
                self.independent_variable.to_numpy()[i : i + window + 1].reshape(-1, 1),
                self.dependent_variable.to_numpy()[i : i + window + 1],
            )

            betas[i + window] = model.coef_[0]
            alphas[i + window] = model.intercept_

        self.rolling_beta = pd.Series(data=betas, index=self.independent_variable.index)

    @property
    def data(self):
        """
        Returns
        -------
        pd.Series : The rolling beta series
        """
        return self.rolling_beta

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        self.rolling_beta.plot(lw=2, x_compat=False, ax=ax, **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha="center")

        ax.xaxis.set_tick_params(reset=True)
        ax.xaxis.set_major_locator(mdates.YearLocator(1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.legend(loc="best")

        ax.set_title(f"Rolling Beta - {self.window}", fontweight="bold")
        return ax
