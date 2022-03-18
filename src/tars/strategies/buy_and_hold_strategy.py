from typing import NoReturn

from pandas import DataFrame, Timestamp

from .abstract_strategy import AbstractStrategy
from ..evaluators import TraderEvaluator
import logging



class BuyAndHold(AbstractStrategy):
    """
    The buy and hold strategy is the reference strategy needed in all
    scenario of comparison as it allows for setting the baseline.

    :param trader: Trader
        The Trader handling a portfolio
    :param pair: str
        The pair e.g. XETHZUSD to buy and hold
    :param volume: float
        The volume of the pair's quote buy
    :param validate: boolean
        Safety Boolean to make sure not to trade real money by default

    :ivar has_run: boolean
        Boolean describing if the strategy has run or not yet.
    :ivar evaluator: AbstractEvaluator
        Evaluator allows for the evaluation of a strategy
    """

    def __init__(self, trader, pair, volume, validate=True):
        self.name = 'Buy and hold'
        self.trader = trader
        self.pair = pair
        self.volume = volume
        self.validate = validate
        self.has_run = False
        self.evaluator = TraderEvaluator(self.trader)

    def run(self) -> NoReturn:
        """ Run the strategy """
        # Checkpoint
        balance = self.trader.portfolio.get_trade_balance().loc['eb'].ZUSD   
        self.evaluator.add_checkpoint(Timestamp.utcnow(), balance)

        # Run strategy
        if not self.has_run:
            self.trader.add_order(pair=self.pair, type='buy',
                                  ordertype='market', volume=self.volume,
                                  validate=self.validate)
            self.has_run = True

    def test(self, dtime: Timestamp, data: DataFrame):
        """ Test the strategy """
        # Checkpoint
        balance = self.trader.portfolio.get_trade_balance(dtime).loc['eb'].ZUSD
        self.evaluator.add_checkpoint(dtime, balance)

        # Run strategy
        if not self.has_run:
            self.trader.add_order(dtime=dtime, pair=self.pair, type='buy',
                                  ordertype='market', volume=self.volume,
                                  validate=self.validate)
            self.has_run = True
