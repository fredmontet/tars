import logging
import pandas as pd
from .abstract_portfolio import AbstractPortfolio


class VirtualPortfolio(AbstractPortfolio):

    def __init__(self, account):
        self.account = account

    def get_account_balance(self):
        return pd.DataFrame.from_dict(self.account, orient='index',
                                      columns=['vol'])

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
