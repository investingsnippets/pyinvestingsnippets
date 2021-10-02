import numpy as np
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

        self.independent_variable = independent_variable.dropna()
        self.dependent_variable = dependent_variable.dropna()

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
