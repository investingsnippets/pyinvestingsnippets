import numpy as np
import pandas as pd


class BetaCovariance:
    """
    Given a Returns Series calculates the beta of a Stock over
    the Benchmark index using covariance
    """

    def __init__(self, independent_variable, dependent_variable):
        """
        Parameters
        ----------
        independent_variable : Market Returns
        dependent_variable : Stock Returns
        """
        self._validate(independent_variable, dependent_variable)
        self.independent_variable = independent_variable.dropna()
        self.dependent_variable = dependent_variable.dropna()

    @staticmethod
    def _validate(independent_variable, dependent_variable):
        assert isinstance(independent_variable.index, pd.DatetimeIndex)
        assert isinstance(dependent_variable.index, pd.DatetimeIndex)

    @property
    def beta(self):
        """
        Calculates the beta of a Stock over the Benchmark index using linear regression

        Returns
        -------
        beta: float
        """
        cov = np.cov(self.dependent_variable, self.independent_variable)
        var = np.var(self.independent_variable)
        return cov[1, 0] / var
