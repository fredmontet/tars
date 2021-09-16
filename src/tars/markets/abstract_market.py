from abc import ABC, abstractmethod


class AbstractMarket(ABC):
    """
    The AbstractMarket provides the method contract to create Market classes.
    Given an exchange, the access to the its information should be similar.
    """

    @abstractmethod
    def get_ohlc_data(self, *args, **kwargs):
        """ Get OHLC data """
        pass

    @abstractmethod
    def get_asset_info(self, *args, **kwargs):
        """ Get information about a specific asset """
        pass

    @abstractmethod
    def get_tradable_asset_pairs(self, *args, **kwargs):
        """ Get information about a pair like USDBTC """
        pass

    @abstractmethod
    def get_ticker_information(self, *args, **kwargs):
        """ Get the latest ticker information about a pair """
        pass

    @abstractmethod
    def get_order_book(self, *args, **kwargs):
        """ Get all latest orders in the Matket for a trade """
        pass

    @abstractmethod
    def get_recent_trades(self, *args, **kwargs):
        """ Get the last executed trades """
        pass

    @abstractmethod
    def get_recent_spread_data(self, *args, **kwargs):
        """ Get the last spread data """
        pass
