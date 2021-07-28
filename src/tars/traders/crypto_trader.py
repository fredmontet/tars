from src.tars.traders.abstract_trader import AbstractTrader
import krakenex
from pykrakenapi import KrakenAPI


class CryptoTrader(AbstractTrader):
    """
    https://docs.kraken.com/rest/#tag/User-Trading
    """
    
    def __init__(self, portfolio, api_key=None):
        api = krakenex.API()
        api.load_key(api_key)
        self.api = KrakenAPI(api)
        self.portfolio = portfolio
        
    def add_order(self, pair, type, ordertype, volume, price=None,
                        price2=None, leverage=None, oflags=None, starttm=0,
                        expiretm=0, userref=None, validate=True,
                        close_ordertype=None, close_price=None,
                        close_price2=None, otp=None,
                        trading_agreement='agree'):
        return self.api.add_standard_order(pair, type, ordertype, volume, price,
                        price2, leverage, oflags, starttm, expiretm, userref, 
                        validate, close_ordertype, close_price, close_price2, 
                        otp, trading_agreement)
    
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


        
    





    

