import pandas as pd
from darts import TimeSeries
from darts.models import ExponentialSmoothing

from src.tars.evaluators.trader_evaluator import TraderEvaluator
from src.tars.strategies.abstract_strategy import AbstractStrategy
from src.tars.markets.crypto_market import CryptoMarket


class PredictionStrategy(AbstractStrategy):
    """
    Prediction Strategy

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
        self.name = 'Prediction'
        self.trader = trader
        self.pair = pair
        self.volume = volume
        self.validate = validate
        self.evaluator = TraderEvaluator(self.trader)
        self.market = CryptoMarket()

    def run(self):
        """ Run the strategy """
        # 1. Add a checkpoint to the evaluator
        balance = self.trader.portfolio.get_trade_balance().loc['eb'].ZUSD
        self.evaluator.add_checkpoint(pd.Timestamp.utcnow(), balance)

        # 2. Process the data
        market = CryptoMarket()

        # get last frame
        df = market.get_ohlc_data(pair=self.pair, ascending=True, interval=15)[0]

        # preprocessing
        ts = TimeSeries.from_dataframe(df.reset_index(), 'dtime', 'close')

        # modeling
        model = ExponentialSmoothing()
        model.fit(ts)

        # 3. Get the relevant information for trading decision
        prediction = round(model.predict(2).last_value(), 2)
        current = df.iloc[-1]['close']

        # 4. Implement the trading logic
        if prediction < current:
            self.trader.add_order(pair=self.pair, type='sell',
                                  ordertype='market', volume=self.volume,
                                  validate=self.validate)

        elif prediction >= current:
            self.trader.add_order(pair=self.pair, type='buy',
                                  ordertype='market', volume=self.volume,
                                  validate=self.validate)
        else:
            pass
