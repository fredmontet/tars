import pandas as pd
from .abstract_portfolio import AbstractPortfolio


class VirtualPortfolio(AbstractPortfolio):

    def __init__(self, account):
        self.account = account

    def get_account_balance(self):
        return pd.DataFrame.from_dict(self.account, orient='index',
                                      columns=['vol'])

    def add_asset(self, name, volume):
        if name in self.account:
            self.account[name] += volume
        else:
            self.account[name] = volume
