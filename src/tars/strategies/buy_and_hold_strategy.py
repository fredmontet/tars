from src.tars.strategies.abstract_strategy import AbstractStrategy

class BuyAndHold(AbstractStrategy):
    
    def __init__(self, trader, pair, amount):
        self.trader = trader
        self.amount = amount
        self.pair = pair
        self.has_run = False

    def run(self):
        if self.has_run == False:
            self.trader.add_order(self.pair, 'buy', self.amount)
            self.has_run = True
