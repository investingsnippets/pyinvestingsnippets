import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


class ExponantiallyWeightedDownsideRisk:
    """A measure of variability derived from volatility of returns is
    the downside risk, the volatility computed only on negative returns
    (or returns below a given threshold)
    """

    def __init__(self, pandas_obj, decay_factor=0.05, window=252) -> None:
        self.decay_factor = decay_factor
        self.window = window
        self.downside_risk = (
            pandas_obj[pandas_obj < 0]
            .ewm(alpha=decay_factor)
            .std()
            .apply(lambda x: x * window ** 0.5)
        )

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        to_plot = self.downside_risk * 100
        to_plot.plot(lw=2, x_compat=True, ax=ax, **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.xaxis.set_tick_params(reset=True)
        ax.tick_params(axis='x', labelrotation=45)
        if 'label' in kwargs:
            ax.legend(loc="best")

        ax.set_title(
            f"Exp. weighted downside risk ({self.window}) \
    \n- Decay factor {self.decay_factor}",
            fontweight="bold",
        )
        return ax
