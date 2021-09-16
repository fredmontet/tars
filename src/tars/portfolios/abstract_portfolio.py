from pandas import DataFrame
from abc import ABC, abstractmethod
import copy


class AbstractPortfolio(ABC):
    """
    The AbstractPortfolio represents the method contract of a portfolio of
    securities.
    """
            
    @abstractmethod
    def get_account_balance(self, *args, **kwargs) -> DataFrame:
        """ Retrieve the balance for each security
        :return account: DataFrame
        """
        pass

    @abstractmethod
    def get_trade_balance(self, *args, **kwargs) -> DataFrame:
        """ Retrieve the available balance in a FIAT currency
        :return trades: DataFrame
        """

        pass
    
    def copy(self):
        """ Create a deep copy of the current Portfolio object
        :return portfolio: Portfolio
        """
        return copy.deepcopy(self)
