from abc import ABC, abstractmethod


class AbstractTrader(ABC):
    """
    The AbstractTrader represents the method contract of a trader aiming at
    making orders and more.
    """

    @abstractmethod
    def add_order(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def cancel_order(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_trades_history(self, *args, **kwargs):
        pass
