import pandas as pd
from ta.trend import MACD

from src.tars.evaluators.trader_evaluator import TraderEvaluator
from src.tars.strategies.abstract_strategy import AbstractStrategy
from src.tars.markets.crypto_market import CryptoMarket


class TrendFollowingMACD(AbstractStrategy):
    
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

        ## process data
        market = CryptoMarket()
        df0 = market.get_ohlc_data(pair=self.pair)[0]['close'].iloc[::-1]

        macd = MACD(df0)
        line = macd.macd()[-1]
        signal = macd.macd_signal()[-1]

        if signal < line:
            self.trader.add_order(pair=self.pair, type='buy',
                                  ordertype='market', volume=self.volume,
                                  validate=self.validate)
        elif line >= signal:
            self.trader.add_order(pair=self.pair, type='sell',
                                  ordertype='market', volume=self.volume,
                                  validate=self.validate)
        else:
            pass
