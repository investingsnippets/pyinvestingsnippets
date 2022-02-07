from scipy.stats import truncnorm
import numpy as np
import pandas as pd
import datetime

class TestUtlis:

    @staticmethod
    def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
        return truncnorm(
            (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
    
    def gbm(n_years = 10, n_scenarios=1000, mu=0.07, sigma=0.15, steps_per_year=12, s_0=100.0, prices=True):
        """
        Generates finctional stock prices based on Geometric Brownian Motion
        """
        dt = 1/steps_per_year
        n_steps = int(n_years*steps_per_year) + 1
        rets_plus_1 = np.random.normal(loc=(1+mu)**dt, scale=(sigma*np.sqrt(dt)), size=(n_steps, n_scenarios))
        rets_plus_1[0] = 1
        ret_val = s_0*pd.DataFrame(rets_plus_1).cumprod() if prices else rets_plus_1-1
        ret_val = ret_val.iloc[:, 0]  # gets first column
        ret_val.index = pd.bdate_range(end=datetime.datetime.now(), periods=ret_val.shape[0])
        return ret_val
