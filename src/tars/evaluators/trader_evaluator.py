from typing import Any, NoReturn
from pandas import Timestamp, DataFrame
from src.tars.utils.metrics import total_net_profit, profit_factor, average_trade_net_profit


class TraderEvaluator:
    """
    Specialized Evaluator to follow a Trader object

    :param trader: Trader object to track
    :ivar checkpoints: Dict where the data points are stored
    """

    def __init__(self, trader):
        self.trader = trader
        self.checkpoints = {}

    def add_checkpoint(self, dtime: Timestamp, value: Any) -> NoReturn:
        """ Add a checkpoint

        :param dtime: Pandas Timestamp of the current time
        :param value: Any value to store
        """
        self.checkpoints[dtime] = [value]

    def evaluate(self) -> DataFrame:
        """ Evaluate the stored data by computing some useful statistics
        e.g. Total net profit, profit factor, etc.

        :return: Pandas DataFrame of the data
        """
        df = DataFrame.from_dict(self.checkpoints, orient='index', columns=['value'])
        df['total net profit'] = df.apply(lambda row: total_net_profit(row['value'], df.iloc[0][0]), axis=1)
        df['profit factor'] = df.apply(lambda row: profit_factor(row['value'], df.iloc[0][0]), axis=1)
        n_trades = len(self.trader.get_trades_history()[0])
        df['average trade net profit'] = df.apply(lambda row: average_trade_net_profit(row['total net profit'], n_trades), axis=1)
        return df
