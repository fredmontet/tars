

def total_net_profit(gross_profit, gross_loss):
    """
    Gross Profit − Gross Loss = Total Net Profit
    
    https://www.investopedia.com/articles/fundamental-analysis/10/strategy-performance-reports.asp
    """
    return gross_profit - gross_loss


def profit_factor(gross_profit, gross_loss):
    """
    Gross Profit / Gross Loss = Profit Factor
    """
    return gross_profit / gross_loss


def percent_profitable(winning_trades, total_trades):
    """
    Winning Trades / Total Trades = Percent Profitable
    """
    return winning_trades / total_trades


def average_trade_net_profit(total_net_profit, total_trades):
    """
    Total Net Profit / Total Trades = Trade Net Profit
    """
    return total_net_profit / total_trades


def win_loss_ratio(winning_trades, losing_trades):
    """
    Winning Trades / Losing Trades

    https://www.investopedia.com/terms/w/win-loss-ratio.asp
    """
    return winning_trades / losing_trades