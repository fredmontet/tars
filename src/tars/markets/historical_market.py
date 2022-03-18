from typing import Tuple

from pandas import DataFrame, Timestamp
import numpy as np

from .abstract_market import AbstractMarket
from .crypto_market import CryptoMarket


class HistoricalMarket(AbstractMarket):

    def __init__(self):
        self.data = {}

    def load(self, pair: str, data: DataFrame):
        self.data[pair] = data

    def get_ohlc_data(self, pair: str, ascending: bool = False) \
            -> Tuple[DataFrame, int]:
        """ Get OHLC data """
        df = self.data[pair].sort_index(ascending=ascending)
        df.index.name = 'dtime'
        df['time'] = df.index.astype(np.int64) // 10**9
        df = df.rename(columns={'trades': 'count'})
        timestamp = df.iloc[0].name.timestamp()
        return df, timestamp

    def get_asset_info(self, *args, **kwargs):
        """ Get information about a specific asset """
        raise NotImplementedError

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
        return CryptoMarket().get_tradable_asset_pairs(info, pair)

    def get_ticker_information(self, timestamp: Timestamp, pair: str):
        """ Get the latest ticker information about a pair """
        tick = self.data[pair].loc[timestamp]
        tick = tick.rename(index={
            'open': 'o',
            'close': 'c',
            'high': 'h',
            'low': 'l',
            'volume': 'v',
            'trades': 't'
        })
        return tick

    def get_order_book(self, *args, **kwargs):
        """ Get all latest orders in the Market for a trade """
        raise NotImplementedError

    def get_recent_trades(self, *args, **kwargs):
        """ Get the last executed trades """
        raise NotImplementedError

    def get_recent_spread_data(self, *args, **kwargs):
        """ Get the last spread data """
        raise NotImplementedError
