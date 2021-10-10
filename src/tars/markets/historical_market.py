from typing import Tuple

from pandas import DataFrame, Timestamp
import numpy as np

from .abstract_market import AbstractMarket


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

    def get_tradable_asset_pairs(self, *args, **kwargs):
        """ Get information about a pair like USDBTC """
        raise NotImplementedError

    def get_ticker_information(self, pair: str, timestamp: Timestamp):
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
