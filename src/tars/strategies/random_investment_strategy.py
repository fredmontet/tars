import random
import pandas as pd

from src.tars.evaluators.trader_evaluator import TraderEvaluator
from src.tars.strategies.abstract_strategy import AbstractStrategy

class RandomInvestment(AbstractStrategy):
    
    def __init__(self, trader, pair, amount):
        self.trader = trader
        self.pair = pair
        self.amount = amount
        self.evaluator = TraderEvaluator(self.trader)

        
    def run(self):
        # Checkpoint
        balance = self.trader.portfolio.get_trade_balance().loc['eb'].ZUSD   
        self.evaluator.add_checkpoint(pd.Timestamp.now(), balance)
        # Run strategy
        order_type = ['buy', 'sell'][random.getrandbits(1)]        
        self.trader.add_order(self.pair, order_type, self.amount)
        