from abc import ABC, abstractmethod


class AbstractTrader(ABC):

    @abstractmethod
    def add_order(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def cancel_order(self, *args, **kwargs):
        pass
