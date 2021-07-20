from abc import ABC, abstractmethod


class AbstractStrategy(ABC):
    
    def __init__(self, market, trader, portfolio):
        self.market = market
        self.trader = trader
        self.portfolio = portfolio
        
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass
    
    