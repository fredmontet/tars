import time
import pandas as pd

from src.tars.evaluators.trader_evaluator import TraderEvaluator
from src.tars.strategies.abstract_strategy import AbstractStrategy


class SequentialInvestment(AbstractStrategy):
    """
    The sequential investment mimics saving money for a period of time,
    investing each month with a fixed account.

    :param trader: Trader
        The Trader handling a portfolio
    :param pair: str
        The pair e.g. XETHZUSD to buy and hold
    :param volume: float
        The volume of the pair's quote buy
    :param n_step: int
        Total number of steps to reach the volume
    :param duration: str
        Duration between two steps encoded in the same way as for Pandas' Timestamp
    :param validate: boolean
        Safety Boolean to make sure not to trade real money by default

    :ivar current_step: int
        The current investment step
    :ivar has_run: boolean
        Boolean describing if the strategy has run or not yet.
    :ivar evaluator: Evaluator
        Evaluator allows for the evaluation of a strategy
    """
    
    def __init__(self, trader, pair, volume, n_step, duration, validate=True):
        self.name = 'Sequential Investment'
        self.trader = trader
        self.pair = pair
        self.volume = volume
        self.n_step = n_step
        self.duration = pd.Timedelta(duration)
        self.validate = validate
        self.current_step = 0
        self.has_run = False
        self.evaluator = TraderEvaluator(self.trader)
        
    def run(self):
        """ Run the strategy """
        # Checkpoint
        balance = self.trader.portfolio.get_trade_balance().loc['eb'].ZUSD   
        self.evaluator.add_checkpoint(pd.Timestamp.utcnow(), balance)
        # Run strategy
        if self.has_run == False:
            step_volume = self.volume / self.n_step
            step_duration = self.duration / self.n_step
            for step in range(self.n_step):
                self.trader.add_order(pair=self.pair, type='buy',
                                      ordertype='market', volume=step_volume,
                                      validate=self.validate)
                self.current_step += 1
                time.sleep(step_duration.total_seconds())
            self.has_run = True