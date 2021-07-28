import pandas as pd
import copy

from src.tars.evaluators.trader_evaluator import TraderEvaluator
from src.tars.strategies.abstract_strategy import AbstractStrategy

class BuyAndHold(AbstractStrategy):
    
    def __init__(self, trader, pair, volume, validate=True):
        self.trader = trader
        self.pair = pair
        self.volume = volume
        self.validate = validate
        self.has_run = False
        self.evaluator = TraderEvaluator(self.trader)
        

    def run(self):
        # Checkpoint
        balance = self.trader.portfolio.get_trade_balance().loc['eb'].ZUSD   
        self.evaluator.add_checkpoint(pd.Timestamp.now(), balance)
        # Run strategy
        if self.has_run == False:
            self.trader.add_order(pair=self.pair, type='buy', ordertype='market', volume=self.volume, validate=self.validate)
            self.has_run = True
