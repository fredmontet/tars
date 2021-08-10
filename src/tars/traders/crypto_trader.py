from typing import Tuple

from pandas import DataFrame

from src.tars.traders.abstract_trader import AbstractTrader
import krakenex
from pykrakenapi import KrakenAPI


class CryptoTrader(AbstractTrader):
    """
    CryptoTrader represents a trader of managing a portfolio of
    cryptocurrencies. It uses the method available from the Kraken API
    (https://docs.kraken.com/rest/#tag/User-Trading).

    :param portfolio: AbstractPortfolio
        The portfolio to trade with
    :param api_key: str
        The API key from Kraken

    :ivar api: KrakenAPI object
    :ivar portfolio: AbstractPortfolio object
    """
    
    def __init__(self, portfolio, api_key=None):
        api = krakenex.API()
        api.load_key(api_key)
        self.api = KrakenAPI(api)
        self.portfolio = portfolio
        
    def add_order(self, pair: str, type: str, ordertype: str, volume: str,
                  price: str = None, price2: str = None,
                  leverage: str = None, oflags: str = None, starttm: int = 0,
                  expiretm: int = 0, userref: int = None, validate: bool = True,
                  close_ordertype=None, close_price=None, close_price2=None,
                  otp: str = None, trading_agreement: str = 'agree') -> dict:
        """ Add a standard order.

        Add a standard order and return an order description info and an array
        of transaction ids for the order (if succesfull).

        :param pair : str
            Asset pair
        :param type : str
            Type of order (buy/sell).
        :param ordertype : str
            Order type, one of:
            market
            limit (price = limit price)
            stop-loss (price = stop loss price)
            take-profit (price = take profit price)
            stop-loss-profit (price = stop loss price, price2 = take profit
                price)
            stop-loss-profit-limit (price = stop loss price, price2 = take
                profit price)
            stop-loss-limit (price = stop loss trigger price, price2 =
                triggered limit price)
            take-profit-limit (price = take profit trigger price, price2 =
                triggered limit price)
            trailing-stop (price = trailing stop offset)
            trailing-stop-limit (price = trailing stop offset, price2 =
                triggered limit offset)
            stop-loss-and-limit (price = stop loss price, price2 = limit price)
            settle-position
        :param volume : str
            Order volume in lots. For minimum order sizes, see
            https://support.kraken.com/hc/en-us/articles/205893708
        :param price : str, optional (default=None)
            Price (optional). Dependent upon ordertype
        :param price2 : str, optional (default=None)
            Secondary price (optional). Dependent upon ordertype
        :param leverage : str, optional (default=None)
            Amount of leverage desired (optional). Default = none
        :param oflags : str, optional (default=None)
            Comma delimited list of order flags:
            viqc = volume in quote currency (not available for leveraged
                orders)
            fcib = prefer fee in base currency
            fciq = prefer fee in quote currency
            nompp = no market price protection
            post = post only order (available when ordertype = limit)
        :param starttm : int, optional (default=None)
            Scheduled start time:
            0 = now (default)
            +<n> = schedule start time <n> seconds from now
            <n> = unix timestamp of start time
        :param expiretm : int, optional (default=None)
            Expiration time:
            0 = no expiration (default)
            +<n> = expire <n> seconds from now
            <n> = unix timestamp of expiration time
        :param userref : int, optional (default=None)
            User reference id.  32-bit signed number.
        :param validate : bool, optional (default=True)
            Validate inputs only. Do not submit order (default).
        :param optional closing order to add to system when order gets filled:
            close[ordertype] = order type
            close[price] = price
            close[price2] = secondary price
        :param otp : str
            Two-factor password (if two-factor enabled, otherwise not required)
        :param trading_agreement : str

        :return res : dict
            res['descr'] = order description info
                order = order description
                close = conditional close order description (if conditional
                    close set)
            res['txid'] = array of transaction ids for order (if order was
                added successfully)
        """
        return self.api.add_standard_order(
            pair, type, ordertype, volume, price, price2, leverage, oflags,
            starttm, expiretm, userref, validate, close_ordertype, close_price,
            close_price2, otp, trading_agreement)
    
    def cancel_order(self, txid: str, otp: str = None) -> Tuple[int, bool]:
        """ Cancel open order(s).

        Cancel open order with transaction id ``txid``.

        :param txid : str
            Transaction id.
        :param otp : str
            Two-factor password (if two-factor enabled, otherwise not required)

        :return Tuple[int, bool]
            count : int
                Number of orders canceled.
            pending : bool
                If set, order(s) is/are pending cancellation.
        """
        return self.api.cancel_open_order(txid, otp)
        
    def get_open_orders(self, trades: bool = False, userref: int = None,
                        otp: str = None) -> DataFrame:
        """ Get open orders info.

        Return a dictionary of open orders info.

        :param trades : bool, optional (default=False)
            Whether or not to include trades in output.
        :param userref : int, optional (default=None)
            Restrict results to given user reference id.
        :param otp : str
            Two-factor password (if two-factor enabled, otherwise not required)

        :return open : DataFrame
        """
        return self.api.get_open_orders(trades, userref, otp)
        
    def get_closed_orders(self, trades: bool = False, userref: int = None,
                          start: int = None, end: int = None, ofs=None,
                          closetime: str = None, otp: str = None) -> DataFrame:
        """ Get closed orders info.

        Return a ``DataFrame`` of closed orders info.

        :param trades : bool, optional (default=False)
            Whether or not to include trades in output.
        :param userref : int, optional (default=None)
            Restrict results to given user reference id.
        :param start : int, optional (default=None)
            Starting unixtime or order tx id of results (exclusive).
        :param end : int, optional (default=None)
            Ending unixtime or order tx id of results (inclusive)-
        :param ofs : ?, optional (default=None)
            Result offset.
        :param closetime : str, optional (default=None)
            Which time to use, must be one of {'open', 'close', 'both'}. If
            None (default), closetime='both'.
        :param otp : str
            Two-factor password (if two-factor enabled, otherwise not required)
        :return: DataFrame
        """
        return self.api.get_closed_orders(trades, userref, start, end, ofs,
                                          closetime, otp)
        
    def query_orders_info(self, txid: str, trades: bool = False,
                          userref: int = None, otp: str = None) \
            -> DataFrame:
        """ Query orders info.

        Return a ``DataFrame`` of orders info.

        :param txid : str
            Comma delimited list of transaction ids to query info about
            (20 maximum).
        :param trades : bool, optional (default=False)
            Whether or not to include trades in output.
        :param userref : int, optional (default=None)
            Restrict results to given user reference id.
        :param otp : str
            Two-factor password (if two-factor enabled, otherwise not required)

        :return orders : DataFrame
            order_txid = order info.  See get_open_orders/get_closed_orders.
        """
        return self.api.query_orders_info(txid, trades, userref, otp)
    
    def get_trades_history(self, type: str = 'all', trades: bool = False,
                           start: int = None, end: int = None, ofs=None,
                           otp: str = None, ascending: bool = False) \
            -> DataFrame:
        """ Get trades history.

        Return a ``DataFrame`` of the trade history.

        :param type : str, optional (default='all')
            Type of trade, must be one of:
                'all' (default)    : all types (default)
                'any position'     : any position (open or closed)
                'closed position'  : positions that have been closed
                'closing position' : any trade closing all or part of a
                                     position
                'no position'      : non-positional trades
        :param trades : bool, optional (default=False)
            Whether or not to include trades related to position in output.
        :param start : int, optional (default=None)
            Starting unixtime or trade tx id of results (exclusive).
        :param end : int, optional (default=None)
            Ending unixtime or trade tx id of results (inclusive).
        :param ofs : ?, optional (default=None)
            Result offset.
        :param otp : str
            Two-factor password (if two-factor enabled, otherwise not required)
        :param ascending : bool, optional (default=False)
            If set to True, the data frame will be sorted with the most recent
            date in the last position. When set to False, the most recent date
            is in the first position.

        :return trades : DataFrame
        """
        return self.api.get_trades_history(type, trades, start, end, ofs, otp,
                                           ascending)
        
    def query_trades_info(self, txid: str, trades: bool = False,
                          otp: str = None, ascending: bool = False) \
            -> DataFrame:
        """ Query trades info.

        Return a ``DataFrame`` of trades info.

        :param txid : str
           Comma delimited list of transaction ids to query info about
           (20 maximum).
        :param trades : bool, optional (default=False)
           Whether or not to include trades related to position in output.
        :param otp : str
           Two-factor password (if two-factor enabled, otherwise not required)
        :param ascending : bool, optional (default=False)
           If set to True, the data frame will be sorted with the most recent
           date in the last position. When set to False, the most recent date
           is in the first position.

        :return trades : DataFrame
        """
        return self.api.query_trades_info(txid, trades, otp, ascending)


        
    





    

