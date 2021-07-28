from time import sleep
from collections import namedtuple
import logging
import uuid

import pandas as pd

from src.tars import portfolios
from src.tars.traders.abstract_trader import AbstractTrader
from src.tars.markets.crypto_market import CryptoMarket

class VirtualCryptoTrader(AbstractTrader):
    """
    https://docs.kraken.com/rest/#tag/User-Trading
    """
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.order_book = {}

    def add_order(self, pair, type, ordertype, volume, validate):
        market = CryptoMarket()

        # 1. Caculate order informations
        dtime = pd.Timestamp.now()
        price = float(market.get_ticker_information(pair)['c'][0][0])
        sleep(1)
        fee_in_percent = market.get_tradable_asset_pairs(info='fees').loc['XETHZUSD']['fees'][0][1] / 100
        sleep(1)
        cost = volume * price
        fee = cost * fee_in_percent
        
        # 2. Update the portfolio
        base, quote = market.get_tradable_asset_pairs(pair=pair)[['base', 'quote']].iloc[0]

        if type == 'buy':
            try: 
                available_quote = self.portfolio.get_account_balance().loc[quote].vol # USD
                if cost <= available_quote:
                    self.portfolio.withdraw(quote, cost + fee) # - USD
                    self.portfolio.deposit(base, volume) # + ETH
            except KeyError:
                logging.error(f'The quote {quote} isn\'t available in the portfolio.')
            except Exception:
                logging.error(f'The cost is higher than the available quote amount.')

        elif type == 'sell':
            try: 
                max_volume = self.portfolio.get_account_balance().loc[base].vol # ETH
                if volume <= max_volume:
                    self.portfolio.withdraw(base, volume) # - ETH
                    self.portfolio.deposit(quote, cost - fee) # + USD
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
    
    def cancel_order(self, order_id):
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

    def get_trades_history(self):
        df = pd.DataFrame.from_dict(self.order_book, orient='index')
        df.reset_index(inplace=True)
        df =    df.rename(columns={'index':'ordertxid'})
        df = df.set_index('dtime')
        return df, len(df)

    def get_total_fees(self):
        fees = sum([v.fee for k,v in self.order_book.items()])
        return round(fees, 2)

VirtualOrder = namedtuple('VirtualOrder', ['dtime', 'pair', 'ordertype', 'type', 'price', 'cost', 'fee', 'volume'])
