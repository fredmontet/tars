import pandas as pd
from scipy.signal import savgol_filter

from src.tars.evaluators.trader_evaluator import TraderEvaluator
from src.tars.strategies.abstract_strategy import AbstractStrategy
from src.tars.markets.crypto_market import CryptoMarket


class TrendFollowing(AbstractStrategy):
    """
    Follow a quote's trend by taking a buy/sell decision based on the 2nd
    derivative of a Savinsky-Golay filtered signal. i.e. :

        sell if dx < negative limit
        buy  if dx > positive limit

    :param trader: Trader
        The Trader handling a portfolio
    :param pair: str
        The pair e.g. XETHZUSD to buy and hold
    :param volume: float
        The volume of the pair's quote buy
    :param validate: boolean
        Safety Boolean to make sure not to trade real money by default

    :ivar evaluator: AbstractEvaluator
        Evaluator allows for the evaluation of a strategy
    :ivar market: AbstractMarket
        Market object to get information from
    """
    
    def __init__(self, trader, pair, volume, validate=True):
        self.name = 'Trend Following with Differential Filter'
        self.trader = trader
        self.pair = pair
        self.volume = volume
        self.validate = validate
        self.evaluator = TraderEvaluator(self.trader)
        self.market = CryptoMarket()

    def run(self):
        """ Run the strategy """
        # Checkpoint
        balance = self.trader.portfolio.get_trade_balance().loc['eb'].ZUSD   
        self.evaluator.add_checkpoint(pd.Timestamp.utcnow(), balance)

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
        pos_lim = 0.9
        neg_lim = -0.9

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
