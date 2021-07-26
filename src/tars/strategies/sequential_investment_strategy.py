import time
import pandas as pd
from src.tars.strategies.abstract_strategy import AbstractStrategy


class SequentialInvestment(AbstractStrategy):
    
    def __init__(self, trader, pair, amount, n_step, duration):
        self.trader = trader
        self.pair = pair
        self.amount = amount
        self.n_step = n_step
        self.duration = pd.Timedelta(duration)
        self.current_step = 0
        self.has_run = False
        
    def run(self):
        if self.has_run == False:
            step_amount = self.amount / self.n_step
            step_duration = self.duration / self.n_step
            for step in range(self.n_step):
                self.trader.add_order(self.pair, 'buy', step_amount)
                self.current_step += 1
                time.sleep(step_duration.total_seconds())
            self.has_run = True