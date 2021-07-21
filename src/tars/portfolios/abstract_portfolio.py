from abc import ABC, abstractmethod


class AbstractPortfolio(ABC):
            
    @abstractmethod
    def get_account_balance(self):
        pass
