from abc import ABC, abstractmethod


class AbstractStrategy(ABC):
        
    @abstractmethod
    def run(self):
        pass
