from threading import Thread
from .utils.runner import Runner


class TARS:
    """
    A trading bot with a name inspired by the movie Interstellar
    """

    def __init__(self):
        self.strategies = []
        self.runners = []
        self.is_running = False

    def start(self, frequency, duration=None):
        """
        Start a trading session

        :param frequency: Timestamp or
        :param duration:
        :return:
        """
        if self.strategies:
            for s in self.strategies:
                runner = Runner()
                self.runners.append(runner)
                thread = Thread(target = runner.start, args =(s.run, frequency, duration))
                thread.start()
            self.is_running = True
    
    def stop(self):
        """ Stop the trading bot """
        if self.runners:
            for r in self.runners:
                r.stop()
                self.runners.remove(r)
            self.is_running = False
    
    def load(self, strategy):
        """ Load a strategy to execute """
        self.strategies.append(strategy)
