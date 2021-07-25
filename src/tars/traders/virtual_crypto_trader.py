from collections import namedtuple
import logging
from src.tars import portfolios
import uuid

from src.tars.traders.abstract_trader import AbstractTrader
from src.tars.markets.crypto_market import CryptoMarket

class VirtualCryptoTrader(AbstractTrader):
    """
    https://docs.kraken.com/rest/#tag/User-Trading
    """
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.order_book = {}

    def add_order(self, pair, type, amount):
        market = CryptoMarket()

        # 1. Create order and add it to the order book
        last_closing_price = float(market.get_ticker_information(pair)['c'][0][0])
        new_order = VirtualOrder(pair, type, amount, last_closing_price)
        order_id = uuid.uuid4().hex[:8]
        self.order_book[order_id] = new_order

        # 2. Update the portfolio
        base, quote = market.get_tradable_asset_pairs(pair=pair)[['base', 'quote']].iloc[0]
        price = amount * last_closing_price # in USD

        if type == 'buy':
            try: 
                available_amount = self.portfolio.get_account_balance().loc[quote].vol # USD
                if price <= available_amount:
                    self.portfolio.withdraw(quote, price) # - USD
                    self.portfolio.deposit(base, amount) # + ETH
            except KeyError:
                logging.error(f'The quote {quote} isn\'t available in the portfolio.')
            except Exception:
                logging.error(f'The price is higher than the available amount.')

        elif type == 'sell':
            try: 
                max_amount = self.portfolio.get_account_balance().loc[base].vol # ETH
                if amount <= max_amount:
                    self.portfolio.withdraw(base, amount) # - ETH
                    self.portfolio.deposit(quote, price) # + USD
            except KeyError:
                logging.error(f'The base {base} isn\'t available in the portfolio.')
            except Exception:
                logging.error(f'The available amount isn\'t available.')

        else:
            logging.error(f'Order type unknown.')
            raise AttributeError
        return new_order
    
    def cancel_order(self, order_id):
        # 1. Update the portfolio
        order = self.order_book[order_id]
        market = CryptoMarket()
        base, quote = market.get_tradable_asset_pairs(pair=order.pair)[['base', 'quote']].iloc[0]
        price = order.amount * order.close

        if order.type == 'buy':
            self.portfolio.deposit(quote, price) # + USD
            self.portfolio.withdraw(base, order.amount) # - ETH
        elif order.type == 'sell':
            self.portfolio.deposit(base, order.amount) # - ETH
            self.portfolio.withdraw(quote, price) # + USD
        else:
            logging.error(f'Order type unknown.')
            raise AttributeError

        # 2. Remove order from order book
        del self.order_book[order_id]

VirtualOrder = namedtuple('VirtualOrder', ['pair', 'type', 'amount', 'close'])
