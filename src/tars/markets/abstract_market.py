from abc import ABC, abstractmethod


class AbstractMarket(ABC):

    @abstractmethod
    def get_ohlc_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_asset_info(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_tradable_asset_pairs(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_ticker_information(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_order_book(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_recent_trades(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_recent_spread_data(self, *args, **kwargs):
        pass
