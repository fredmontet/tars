from abc import ABC, abstractmethod

from pandas import DataFrame, Timestamp


class AbstractStrategy(ABC):
    """
    The AbstractStrategy represents the method contract of a trading
    strategy of taken by a trader to manage a portfolio.
    """

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def test(self, dtime: Timestamp, data: DataFrame):
        pass
