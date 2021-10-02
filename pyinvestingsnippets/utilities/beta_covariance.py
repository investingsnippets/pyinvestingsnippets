import numpy as np


class BetaCovariance:
    """
    Given a Returns Series calculates the beta of a Stock over
    the Benchmark index using using covariance
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
        cov = np.cov(self.dependent_variable, self.independent_variable)
        var = np.var(self.independent_variable)
        return cov[1, 0] / var
