from abc import ABC, abstractmethod


class AbstractEvaluator(ABC):
    """
    The AbstractEvaluator provides the method contract to create Evaluator.
    It is a class aiming at collecting data during a process and evaluating it
    at some point.
    """

    @abstractmethod
    def add_checkpoint(self, *args, **kwargs):
        """ Add a checkpoint during a followed process """
        pass

    @abstractmethod
    def evaluate(self, *args, **kwargs):
        """ Evaluate the process """
        pass
