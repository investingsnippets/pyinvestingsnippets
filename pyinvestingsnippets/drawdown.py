
from pandas import DataFrame

class Drawdown:
    """Given a wealth index DataFrame, will produce usefull drawdown metrics"""

    def __init__(self, df: DataFrame):
        self.wealth_index_df = df
