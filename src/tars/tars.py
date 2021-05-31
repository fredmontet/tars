import krakenex
from pykrakenapi import KrakenAPI


class TARS:
    """
    A trading bot with a name inspired by the movie Interstellar
    """

    def __init__(self, api_key):
        # Init Kraken API
        api = krakenex.API()
        api.load_key(api_key)
        self.kraken = KrakenAPI(api)

    def start(self, dry_run=True):
        """ Start the trading bot """
        print('start')
        pass
        
    def trade(self, quote, dry_run=True):
        """ Execute a trading action given a model output """
        print('trade')
        pass
    
    def rebalance(self, dry_run=True):
        """ Rebalance the portfolio of quotes """
        print('rebalance')
        pass
    
    def load_model(self, model):
        """ Load a model in TARS """
        print('load model')
        pass
    
    def get_performance_report(self, dry_run=True):
        """ Plot a report showing the performance of the bot """
        print('get performance report')
        pass
    
    def get_portfolio(self, dry_run=True):
        """ Plot all quotes in the portfolio managed by the bot """
        print('get portfolio')
        pass


