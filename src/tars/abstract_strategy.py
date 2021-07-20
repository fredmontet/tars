from abc import ABC, abstractmethod


class AbstractStrategy(ABC):
    
    def __init__(market, trader, portfolio):
        self.market = market
        self.trader = trader
        self.portfolio = portfolio
        
    @abstractmethod
    def start():
        pass
    
    @abstractmethod
    def stop():
        pass
    
    