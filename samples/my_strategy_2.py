from tars import portfolios, traders, strategies


def func():
    portfolio = portfolios.VirtualPortfolio({'ZUSD': 1000})
    trader = traders.VirtualCryptoTrader(portfolio)
    strategy = strategies.PredictionStrategy(trader, 'XETHZUSD', 0.2)
    return strategy
