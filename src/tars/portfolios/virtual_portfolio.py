import logging
import pandas as pd
from ..markets import CryptoMarket
from .abstract_portfolio import AbstractPortfolio


class VirtualPortfolio(AbstractPortfolio):

    def __init__(self, account):
        self.account = account

    def get_account_balance(self):
        return pd.DataFrame.from_dict(self.account, orient='index',
                                      columns=['vol']).round(2)

    def get_trade_balance(self, asset='ZUSD'):

        # Get list of crypto assets
        quote = asset
        af = self.get_account_balance()
        currencies = list(af.index)
        if quote in currencies: 
            currencies.remove(quote)

        # Convert all crypto assets in quote currency
        if currencies :
            equity_totals = []
            for c in currencies:
                pair = c + quote
                tf = CryptoMarket().get_ticker_information(pair)
                close = float(tf['c'][0][0])
                available_amount = af['vol'].loc[c]
                total_in_usd = close * available_amount
                equity_totals.append(total_in_usd)
            # Sum everything and return
            total = sum(equity_totals) + af.loc[quote]['vol']
        else: 
            total = af.loc[quote]['vol']

        return pd.DataFrame.from_dict({'eb':[total]}, orient='index', columns=[quote]) 

    def deposit(self, name, volume):
        if name in self.account:
            self.account[name] += volume
        else:
            self.account[name] = volume
    
    def withdraw(self, name, volume):
        try:
            if self.account[name] >= volume:
                self.account[name] -= volume
                if self.account[name] == 0:
                    del self.account[name]
            else:
                logging.error(f'The amount to remove from the portfolio exceeds its content.')
        except KeyError:
            logging.error(f'The key {name} isn\'t in the portfolio')
