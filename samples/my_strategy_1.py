from tars import portfolios, traders, strategies

"""
This sample uses an existing strategy and trades with it.
Results of the strategy execution are in the logfile tars.log
"""

def func():
    portfolio = portfolios.VirtualPortfolio({'ZUSD': 1000})
    trader = traders.VirtualCryptoTrader(portfolio)
    strategy = strategies.BuyAndHold(trader, 'XETHZUSD', 0.2)
    return strategy

