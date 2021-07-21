from src.tars.traders.abstract_trader import AbstractTrader
import logging


class VirtualTrader(AbstractTrader):
    """
    https://docs.kraken.com/rest/#tag/User-Trading
    """
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def add_order(self, pair):
        acc = self.portfolio
        return
    
    def cancel_order(self):
        return 
    

        
    





    

