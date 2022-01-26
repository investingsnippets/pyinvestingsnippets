import matplotlib.pyplot as plt


class RollingBetaCovariance:
    """
    Given a Returns Series calculates the beta.

    Beta = Covariance / Variance: Where covariance is the stock’s
    return relative to the market's return.

    We use covariance in this implementation.
    """

    def __init__(self, independent_variable, dependent_variable, window):
        """
        Calculates the rolling beta of a Stock over the Benchmark index using covariance

        Parameters
        ----------
        independent_variable : Market Returns
        dependent_variable : Stock Returns
        window : rolling window
        """

        self.independent_variable = independent_variable.dropna()
        self.dependent_variable = dependent_variable.dropna()
        self.window = window

        self.rolling_beta = (
            self.dependent_variable.rolling(window).cov(self.independent_variable)
            / self.independent_variable.rolling(window).var()
        )

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

        self.rolling_beta.plot(lw=2, x_compat=True, ax=ax, **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)

        ax.xaxis.set_tick_params(reset=True)
        ax.tick_params(axis='x', labelrotation=45)
        if 'label' in kwargs:
            ax.legend(loc="best")

        ax.set_title(f"Rolling Beta - {self.window}", fontweight="bold")
        return ax
