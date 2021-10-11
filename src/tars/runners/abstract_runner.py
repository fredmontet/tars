from abc import ABC, abstractmethod


class AbstractRunner(ABC):
    """
    The AbstractRunner represents the method contract for a runner.
    """

    @abstractmethod
    def start(self, *args, **kwargs):
        """ Start the runner """
        pass

    @abstractmethod
    def stop(self, *args, **kwargs):
        """ Stop the runner """
        pass
