
class TARS:
    """
    A trading bot with a name inspired by the movie Interstellar
    """

    def __init__(self):
        self.strategy = None
        self.is_running = False

    def start(self):
        """ Start the trading bot """
        if self.strategy is not None:
            self.strategy.start()
            self.is_running = True
    
    def stop(self):
        """ Stop the trading bot """
        if self.strategy is not None:
            self.strategy.stop()
            self.is_running = False
    
    def load(self, strategy):
        """ Load a strategy to execute """
        self.strategy = strategy
