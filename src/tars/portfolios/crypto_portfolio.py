import krakenex
from pandas import DataFrame
from pykrakenapi import KrakenAPI
from .abstract_portfolio import AbstractPortfolio


class CryptoPortfolio(AbstractPortfolio):
    """
    CryptoPortfolio is a portfolio of cryptocurrencies. It takes its data from
    the Kraken API and provides methods to show the portfolio with different
    focuses.

    :param api_key: str
        The API key from Kraken

    :ivar api: KrakenAPI object
    """

    def __init__(self, api_key: str):
        api = krakenex.API()
        api.load_key(api_key)
        self.api = KrakenAPI(api)

    def get_account_balance(self, otp: str = None) -> DataFrame:
        """ Get asset names and balance amount.

        :param otp: str
            Two-factor password (if two-factor enabled, otherwise not required)

        :return: DataFrame
        """
        return self.api.get_account_balance(otp)
    
    def get_trade_balance(self, aclass: str = 'currency', asset: str = 'ZUSD',
                          otp: str = None) -> DataFrame:
        """Get trade balance info.


        :param aclass: str, optional (default='currency')
            Asset class.
        :param asset:  str, optional (default='ZUSD')
            Base asset used to determine balance.
        :param otp: str
            Two-factor password (if two-factor enabled, otherwise not required)

        :return: DataFrame
        """
        return self.api.get_trade_balance(aclass, asset, otp)


