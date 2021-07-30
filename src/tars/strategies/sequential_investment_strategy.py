import time
import pandas as pd

from src.tars.evaluators.trader_evaluator import TraderEvaluator
from src.tars.strategies.abstract_strategy import AbstractStrategy

class SequentialInvestment(AbstractStrategy):
    
    def __init__(self, trader, pair, volume, n_step, duration, validate=True):
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
        # Checkpoint
        balance = self.trader.portfolio.get_trade_balance().loc['eb'].ZUSD   
        self.evaluator.add_checkpoint(pd.Timestamp.utcnow(), balance)
        # Run strategy
        if self.has_run == False:
            step_volume = self.volume / self.n_step
            step_duration = self.duration / self.n_step
            for step in range(self.n_step):
                self.trader.add_order(pair=self.pair, type='buy', ordertype='market', volume=step_volume, validate=self.validate)
                self.current_step += 1
                time.sleep(step_duration.total_seconds())
            self.has_run = True