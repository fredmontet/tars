import random
from src.tars.strategies.abstract_strategy import AbstractStrategy

class RandomInvestment(AbstractStrategy):
    
    def __init__(self, trader, pair, amount):
        self.trader = trader
        self.pair = pair
        self.amount = amount
        
    def run(self):
        order_type = ['buy', 'sell'][random.getrandbits(1)]        
        self.trader.add_order(self.pair, order_type, self.amount)
        