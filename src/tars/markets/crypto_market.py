from typing import Tuple
from pandas import DataFrame

from .abstract_market import AbstractMarket
import krakenex
from pykrakenapi import KrakenAPI


class CryptoMarket(AbstractMarket):
    """
    The CryptoMarket class allows to get data from the cryptocurrency
    market through Kraken Exchange.

    The full specifications about the methods available in the Kraken API
    is here : https://docs.kraken.com/rest/#tag/Market-Data

    For the full docstrings of the methods, check the Pykrakenapi package
    on GitHub : https://github.com/dominiktraxl/pykrakenapi/blob/master/pykrakenapi/pykrakenapi.py

    :ivar api: KrakenAPI object on public data
    """
    
    def __init__(self):
        self.api = KrakenAPI(krakenex.API())
            
    def get_ohlc_data(self, pair: str, interval: int = 1, since: int = None,
                      ascending: bool = False) -> Tuple[DataFrame, int]:
        """ Get OHLC data for a given pair

        :param pair: str
            Asset pair to get OHLC data for.
        :param interval: int, optional (default=1)
            Time frame interval in minutes. Defaults to 1. One of
            {1, 5, 15, 30, 60, 240, 1440, 10080, 21600}.
        :param since: int, optional (default=None)
            Return committed OHLC data since given unixtime (exclusive). If
            None, retrieve from earliest time possible.
        :param ascending : bool, optional (default=False)
            If set to True, the data frame will be sorted with the most recent
            date in the last position. When set to False, the most recent date
            is in the first position.

        :return ohlc: Tuple[DataFrame, int]
        """
        return self.api.get_ohlc_data(pair=pair, interval=interval, since=since,
                                      ascending=ascending)
    
    def get_asset_info(self, info=None, aclass: str = None, asset: str = None) \
            -> DataFrame:
        """ Get information about a specific asset

        Available assets : https://support.kraken.com/hc/en-us/articles/360000678446-Cryptocurrencies-available-on-Kraken

        :param info: ?, optional (default=None)
            Info to retrieve. If None (default), retrieve all info.
        :param aclass: str, optional (default=None)
            Asset class. If None (default), aclass='currency'.
        :param asset: str, optional (default=None)
            Comma delimited list of assets to get info on. If None (default),
            all for given asset class.

        :return asset: DataFrame
        """
        return self.api.get_asset_info(info, aclass, asset)
    
    def get_tradable_asset_pairs(self, info: str = None, pair: str = None) \
            -> DataFrame:
        """Get tradable asset pairs.

        Return a ``DataFrame`` of pair names and their info.

        :param info: str, optional (default=None)
            Info to retrieve. Can be one of {'leverage', 'fees', 'margin'}.
            If None (default), retrieve all info.
        :param pair: str, optional (default=None)
            Comma delimited list of asset pairs to get info on. If None
            (default), all.

        :return pairs: DataFrame
        """
        return self.api.get_tradable_asset_pairs(info, pair)

    def get_ticker_information(self, pair: str) -> DataFrame:
        """Get ticker information.

        Return a ``DataFrame`` of pair names and their ticker info.

        :param pair: str
            Comma delimited list of asset pairs to get info on.

        :return ticker: DataFrame
        """
        return self.api.get_ticker_information(pair)
    
    def get_order_book(self, pair, count: int = 100, ascending: bool = False) \
            -> Tuple[DataFrame, DataFrame]:
        """ Get order book (market depth).

        Return a ``DataFrame`` for both asks and bids for a given pair.

        :param pair: str
            Asset pair to get market depth for.
        :param count: int, optional (default=100)
            Maximum number of asks/bids. Per default, get the latest 100
            bids and asks.
        :param ascending: bool, optional (default=False)
            If set to True, the data frame will be sorted with the most recent
            date in the last position. When set to False, the most recent date
            is in the first position.

        :return order_book: DataFrame
        """
        return self.api.get_order_book(pair, count, ascending)
    
    def get_recent_trades(self, pair: str, since: int = None,
                          ascending: bool = False) -> Tuple[DataFrame, int]:
        """ Get recent trades data.

        Return a ``DataFrame`` of recent trade data for a given pair,
        optionally from ``since`` onwards (exclusive).

        :param pair: str
            Asset pair to get trade data for.
        :param since: int, optional (default=None)
            Return trade data since given unixtime (exclusive). If
            None, retrieve from earliest time possible.
        :param ascending: bool, optional (default=False)
            If set to True, the data frame will be sorted with the most recent
            date in the last position. When set to False, the most recent date
            is in the first position.

        :return trades: DataFrame
        """
        return self.api.get_recent_trades(pair, since, ascending)
    
    def get_recent_spread_data(self, pair: str, since: int = None,
                               ascending: bool = False) \
            -> Tuple[DataFrame, int]:
        """ Get recent spread data.

        Return a ``DataFrame`` of recent spread data for a given pair,
        optionally from ``since`` onwards (inclusive).

        :param pair: str
            Asset pair to get spread data for.
        :param since: int, optional (default=None)
            Return spread data since given unixtime (inclusive). If
            None, retrieve from earliest time possible.
        :param ascending: bool, optional (default=False)
            If set to True, the data frame will be sorted with the most recent
            date in the last position. When set to False, the most recent date
            is in the first position.

        :return trades: Tuple[DataFrame, int]
        """
        return self.api.get_recent_spread_data(pair, since, ascending)
