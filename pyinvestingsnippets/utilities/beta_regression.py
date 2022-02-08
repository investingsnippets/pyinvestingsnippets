import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class BetaRegression:
    """
    Given a Returns Series calculates the beta of a Stock over
    the Benchmark index using linear regression
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
        x = np.array(self.independent_variable).reshape((-1, 1))
        y = np.array(self.dependent_variable)
        model = LinearRegression().fit(x, y)
        return model.coef_[0]
