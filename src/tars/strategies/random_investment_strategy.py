import random
import pandas as pd

from src.tars.evaluators.trader_evaluator import TraderEvaluator
from src.tars.strategies.abstract_strategy import AbstractStrategy


class RandomInvestment(AbstractStrategy):
    """
    The random strategy is the best way to loose money. It buys or sell
    a security at an unforeseen time.

    :param trader: Trader
        The Trader handling a portfolio
    :param pair: str
        The pair e.g. XETHZUSD to buy and hold
    :param volume: float
        The volume of the pair's quote buy

    :ivar evaluator: Evaluator
        Evaluator allows for the evaluation of a strategy
    """
    
    def __init__(self, trader, pair, volume, validate=True):
        self.name = 'Random Investment'
        self.trader = trader
        self.pair = pair
        self.volume = volume
        self.evaluator = TraderEvaluator(self.trader)
        self.validate = validate

    def run(self):
        """ Run the strategy """
        # Checkpoint
        balance = self.trader.portfolio.get_trade_balance().loc['eb'].ZUSD   
        self.evaluator.add_checkpoint(pd.Timestamp.utcnow(), balance)
        # Run strategy
        type = ['buy', 'sell'][random.getrandbits(1)]
        self.trader.add_order(pair=self.pair, type=type,
                              ordertype='market', volume=self.volume,
                              validate=self.validate)
