from abc import ABC, abstractmethod


class AbstractEvaluator(ABC):

    @abstractmethod
    def add_checkpoint(self, *args, **kwargs):
        pass

    @abstractmethod
    def evaluate(self, *args, **kwargs):
        pass