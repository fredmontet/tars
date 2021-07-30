import pandas as pd
from scipy.signal import savgol_filter

from src.tars.evaluators.trader_evaluator import TraderEvaluator
from src.tars.strategies.abstract_strategy import AbstractStrategy
from src.tars.markets.crypto_market import CryptoMarket


class TrendFollowing(AbstractStrategy):
    
    def __init__(self, trader, pair, volume, validate=True):
        self.trader = trader
        self.pair = pair
        self.volume = volume
        self.validate = validate
        self.evaluator = TraderEvaluator(self.trader)
        self.market = CryptoMarket()

    def run(self):
        # Checkpoint
        balance = self.trader.portfolio.get_trade_balance().loc['eb'].ZUSD   
        self.evaluator.add_checkpoint(pd.Timestamp.now(), balance)

        # Run strategy

        ## parameters
        n = 10
        r = 60
        w = 103
        o = 4

        ## process data
        market = CryptoMarket()
        df0 = market.get_ohlc_data(pair=self.pair)[0]['close'].iloc[::-1]
        df1 = df0.diff(n).diff(n).rolling(r).mean()
        arr = savgol_filter(df1.to_numpy(), w, o)
        df2 = pd.DataFrame(arr).set_index(df1.index)

        ## set thresholds
        dx = df2.iloc[-1][0]
        pos_lim = 0.5
        neg_lim = -0.5

        ## trading rules
        if dx <= neg_lim:
            self.trader.add_order(pair=self.pair, type='sell',
                                  ordertype='market', volume=self.volume,
                                  validate=self.validate)
        elif dx >= pos_lim:
            self.trader.add_order(pair=self.pair, type='buy',
                                  ordertype='market', volume=self.volume,
                                  validate=self.validate)
        else:
            pass
