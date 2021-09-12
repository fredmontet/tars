from time import sleep
from collections import namedtuple
import logging
import uuid
from typing import NoReturn, Tuple

import pandas as pd
from pandas import DataFrame

from src.tars.traders.abstract_trader import AbstractTrader
from src.tars.markets.crypto_market import CryptoMarket


VirtualOrder = namedtuple('VirtualOrder', ['dtime', 'pair', 'ordertype', 'type',
                                           'price', 'cost', 'fee', 'volume'])


class VirtualCryptoTrader(AbstractTrader):
    """
    VirtualCryptoTrader is a paper trader of cryptocurrencies. It allows to try
    things without real financial risks.

    :param portfolio: AbstractPortfolio
        The portfolio to manage

    :ivar order_book: dict
        The book of all virtual orders made by the trader
    """
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.order_book = {}

    def add_order(self, pair: str, type: str, ordertype: str, volume: float, validate) \
            -> VirtualOrder:
        """ Add a virtual standard order.

        Add a virtual standard order and returns it.

        :param pair: str
            Asset pair
        :param type: str
            Type of order (buy/sell).
        :param ordertype: str
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
        :param volume: float
            Order volume in lots. For minimum order sizes, see
            https://support.kraken.com/hc/en-us/articles/205893708

        :return new_order: VirtualOrder
        """

        market = CryptoMarket()

        # 1. Caculate order informations
        dtime = pd.Timestamp.utcnow()
        price = float(market.get_ticker_information(pair)['c'][0][0])
        sleep(1)
        fee_in_percent = market.get_tradable_asset_pairs(info='fees').loc[pair]['fees'][0][1] / 100
        sleep(1)
        cost = volume * price
        fee = cost * fee_in_percent
        
        # 2. Update the portfolio
        base, quote = market.get_tradable_asset_pairs(pair=pair)[['base', 'quote']].iloc[0]

        if type == 'buy':
            try: 
                available_quote = self.portfolio.get_account_balance().loc[quote].vol # USD
                if cost <= available_quote:
                    try:
                        self.portfolio.withdraw(quote, cost + fee)  # - USD
                        self.portfolio.deposit(base, volume)  # + ETH
                    except Exception:
                        pass
            except KeyError:
                logging.error(f'The quote {quote} isn\'t available in the portfolio.')
            except Exception:
                logging.error(f'The cost is higher than the available quote amount.')

        elif type == 'sell':
            try: 
                max_volume = self.portfolio.get_account_balance().loc[base].vol # ETH
                if volume <= max_volume:
                    try:
                        self.portfolio.withdraw(base, volume)  # - ETH
                        self.portfolio.deposit(quote, cost - fee)  # + USD
                    except Exception:
                        pass
            except KeyError:
                logging.error(f'The base {base} isn\'t available in the portfolio.')
            except Exception:
                logging.error(f'The available amount isn\'t available.')

        else:
            logging.error(f'Order type unknown.')
            raise AttributeError

        # 3. Update order book
        new_order = VirtualOrder(dtime, pair, type, ordertype, price, cost, fee, volume)
        order_id = uuid.uuid4().hex[:8]
        self.order_book[order_id] = new_order

        return new_order
    
    def cancel_order(self, order_id) -> NoReturn:
        """ Cancel open order(s).

        Cancel open order with transaction id ``order_id``.

        :param order_id : str
            Transaction id.
        """
        # 1. Update the portfolio
        order = self.order_book[order_id]
        market = CryptoMarket()
        base, quote = market.get_tradable_asset_pairs(pair=order.pair)[['base', 'quote']].iloc[0]

        if order.type == 'buy':
            self.portfolio.deposit(quote, order.cost) # + USD
            self.portfolio.withdraw(base, order.volume) # - ETH
        elif order.type == 'sell':
            self.portfolio.deposit(base, order.volume) # - ETH
            self.portfolio.withdraw(quote, order.cost) # + USD
        else:
            logging.error(f'Order type unknown.')
            raise AttributeError

        # 2. Remove order from order book
        del self.order_book[order_id]

    def get_trades_history(self) -> Tuple[DataFrame, int]:
        """ Get trades history.

        Return a ``DataFrame`` of the trade history.

        :return: Tuple[DataFrame, int]
        """
        df = pd.DataFrame.from_dict(self.order_book, orient='index')
        df.reset_index(inplace=True)
        df = df.rename(columns={'index':'ordertxid'})
        df = df.set_index('dtime')
        return df, len(df)

    def get_total_fees(self):
        """ Get the total sum of fees

        :return fees: float
        """
        fees = sum([v.fee for k,v in self.order_book.items()])
        return round(fees, 2)

