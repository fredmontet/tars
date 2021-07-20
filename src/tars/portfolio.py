import krakenex
from pykrakenapi import KrakenAPI


class Portfolio:
    
    def __init__(self, api_key):
        if api_key is not None:
            self.live = True
            api = krakenex.API()
            api.load_key(api_key)
            self.api = KrakenAPI(api)
        else:
            print('To create a portfolio, you need')
            
    def get_account_balance(self, otp=None):
        return self.api.get_account_balance(otp)
    
    def get_trade_balance(self, aclass='currency',
                          asset='CHF', otp=None):
        return self.api.get_trade_balance(aclass, asset, otp)

    