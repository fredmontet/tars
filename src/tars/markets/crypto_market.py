from .abstract_market import AbstractMarket
import krakenex
from pykrakenapi import KrakenAPI


class CryptoMarket(AbstractMarket):
    """
    https://docs.kraken.com/rest/#tag/Market-Data
    """
    
    def __init__(self):
        api = krakenex.API()
        self.api = KrakenAPI(api)
            
    def get_ohlc_data(self, pair):
        return self.api.get_ohlc_data(pair)
    
    def get_asset_info(self, info=None, aclass=None, asset=None):
        return self.api.get_asset_info(info, aclass, asset)
    
    def get_tradable_asset_pairs(self, info=None, pair=None):
        return self.api.get_tradable_asset_pairs(info, pair)
    
    def get_ticker_information(self, pair):
        return self.api.get_ticker_information(pair)
    
    def get_order_book(self, pair, count=100, ascending=False):
        return self.api.get_order_book(pair, count, ascending)
    
    def get_recent_trades(self, pair, since=None, ascending=False):
        return self.api.get_recent_trades(pair, since, ascending)
    
    def get_recent_spread_data(self, pair, since=None, ascending=False):
        return self.api.get_recent_spread_data(pair, since, ascending)
