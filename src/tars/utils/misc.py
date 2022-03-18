from ..markets.abstract_market import AbstractMarket
from pandas import Series
from difflib import get_close_matches


def get_closest_pairs(pair: str, market: AbstractMarket) -> list:
    """ Given a pair and a market, this method return the closest
    pairs. For instance, if 'ETHZUSD' is given but not available, it
    will return ['ETHUSD', 'XETHTUSD',... ]

    :param pair: str
        The query pair
    :param market: AbstractMarket
        The market to search in
    :return: closest_pairs : List
        The List of closest pairs
    """
    pairs = market.get_tradable_asset_pairs().index.tolist()
    return get_close_matches(pair, pairs)


def get_pair(pair: str, market: AbstractMarket) -> Series:
    """ Get a pair from a market thoroughly. The method looks at
    the different field of the available pairs and if there is a match,
    it returns it.

    :param pair: str
        The pair to get
    :param market: AbstractMarket
        The market to look in

    :return asset_pair: Series
        All informations related to the requested pair
    """
    df = market.get_tradable_asset_pairs()
    try:
        return df.loc[pair]
    except KeyError:
        pass
    try:
        return df.loc[df['altname'] == pair].iloc[0]
    except IndexError:
        closest = get_close_matches(pair, df.index.tolist())
        raise ValueError(f'The requested pair {pair} does not exist, closest matches are {closest}')
