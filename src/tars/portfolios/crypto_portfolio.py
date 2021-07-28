import krakenex
from pykrakenapi import KrakenAPI
from .abstract_portfolio import AbstractPortfolio


class CryptoPortfolio(AbstractPortfolio):
    
    def __init__(self, api_key):
        api = krakenex.API()
        api.load_key(api_key)
        self.api = KrakenAPI(api)

    def get_account_balance(self, otp=None):
        return self.api.get_account_balance(otp)
    
    def get_trade_balance(self, aclass='currency', asset='ZUSD', otp=None):
        return self.api.get_trade_balance(aclass, asset, otp)


