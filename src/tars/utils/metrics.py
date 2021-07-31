"""
Some metrics taken from :
- https://www.investopedia.com/articles/fundamental-analysis/10/strategy-performance-reports.asp
"""


def total_net_profit(gross_profit: float, gross_loss: float) -> float:
    """ Total net profit

    .. math::
        Gross Profit − Gross Loss = Total Net Profit

    :param gross_profit: float of the gross profit
    :param gross_loss: float of the gross loss
    :return: float of the total net profit
    """
    return gross_profit - gross_loss


def profit_factor(gross_profit: float, gross_loss: float) -> float:
    """ Profit factor

    .. math::
        Gross Profit / Gross Loss = Profit Factor

    :param gross_profit: float of the gross profit
    :param gross_loss: float of the gross loss
    :return: float of the profit factor
    """
    return gross_profit / gross_loss


def percent_profitable(winning_trades: int, total_trades: int) -> float:
    """ Percent profitable

    .. math::
        Winning Trades / Total Trades = Percent Profitable

    :param winning_trades: int of the number of winning trades
    :param total_trades: int of the total number of trades executed
    :return: float of the profitability in percent (1.0 = 100%)
    """
    return winning_trades / total_trades


def average_trade_net_profit(total_net_profit: float, total_trades: int) \
        -> float:
    """ Average trade net profit

    .. math::
        Total Net Profit / Total Trades = Trade Net Profit

    :param total_net_profit: float of the total net profit
    :param total_trades: int of the total number of trades executed
    :return float of the average trade net profit
    """
    return total_net_profit / total_trades


def win_loss_ratio(winning_trades: float, losing_trades: float) -> float:
    """ Win/loss ratio

    Taken from https://www.investopedia.com/terms/w/win-loss-ratio.asp

    .. math::
        Winning Trades / Losing Trades = Win Loss Ratio

    :param winning_trades: int of the number of winning trades
    :param losing_trades: int of the number of losing trades
    :return float of the win/loss ratio
    """
    return winning_trades / losing_trades
