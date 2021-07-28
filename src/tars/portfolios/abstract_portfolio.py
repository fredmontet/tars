from abc import ABC, abstractmethod
import copy


class AbstractPortfolio(ABC):
            
    @abstractmethod
    def get_account_balance(self, *args, **kwargs):
        pass
    
    def copy(self):
        return copy.deepcopy(self)
