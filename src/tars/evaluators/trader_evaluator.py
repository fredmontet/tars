from collections import namedtuple
from src.tars.utils.metrics import total_net_profit, profit_factor, average_trade_net_profit
import pandas as pd


class TraderEvaluator:

    def __init__(self, trader):
        self.trader = trader
        self.checkpoints = {}

    def add_checkpoint(self, dtime, value):
        self.checkpoints[dtime] = [value]

    def evaluate(self):
        df = pd.DataFrame.from_dict(self.checkpoints, orient='index', columns=['value'])
        df['total net profit'] = df.apply(lambda row: total_net_profit(row['value'], df.iloc[0][0]), axis=1)
        df['profit factor'] = df.apply(lambda row: profit_factor(row['value'], df.iloc[0][0]), axis=1)
        n_trades = len(self.trader.get_trades_history()[0])
        df['average trade net profit'] = df.apply(lambda row: average_trade_net_profit(row['total net profit'], n_trades), axis=1)
        return df
