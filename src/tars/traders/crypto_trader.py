from src.tars.traders.abstract_trader import AbstractTrader
import logging
import krakenex
from pykrakenapi import KrakenAPI


class CryptoTrader(AbstractTrader):
    """
    https://docs.kraken.com/rest/#tag/User-Trading
    """
    
    def __init__(self, api_key=None):
        if api_key is not None:
            logging.warning('Live mode : on')
            self.live = True
            api = krakenex.API()
            api.load_key(api_key)
            self.api = KrakenAPI(api)
        else:
            self.live = False
            logging.warning('Live mode : off')

    def add_order(self, *args, **kwargs):
        return self.api.add_standard_order(args, kwargs)
    
    def cancel_order(self, txid, otp=None):
        return self.api.cancel_open_order(txid, otp)
        
    def get_open_orders(self, trades=False, userref=None, otp=None):
        return self.api.get_open_orders(trades, userref, otp)
        
    def get_closed_orders(self, trades=False, userref=None, start=None, 
                          end=None, ofs=None, closetime=None, otp=None):
        return self.api.get_closed_orders(trades, userref, start, end, ofs, closetime, otp)
        
    def query_orders_info(self, txid, trades=False, userref=None, otp=None):
        return self.api.query_orders_info(txid, trades, userref, otp)
    
    def get_trades_history(self, type='all', trades=False, start=None,
                           end=None, ofs=None, otp=None, ascending=False):
        return self.api.get_trades_history(type, trades, start, end, ofs, otp, ascending)
        
    def query_trades_info(self, txid, trades=False, otp=None, ascending=False):
        return self.api.query_trades_info(txid, trades, otp, ascending)


        
    





    

