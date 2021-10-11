import logging
from typing import Callable, NoReturn

from pandas import DataFrame

from .abstract_runner import AbstractRunner


class HistoricalRunner(AbstractRunner):
    """
    A HistoricalRunner is an object able to execute a function for each element
    of a DataFrame index.

    :ivar is_running : Boolean describing if the Runner is running or not.
    """

    def __init__(self):
        self.is_running = False

    def start(self, func: Callable, data: DataFrame) \
            -> NoReturn:
        """ Start the Historical Runner

        :param func: The function to be executed
        :param data: Pandas DataFrame containing OHLC data

        """
        self.is_running = True
        for i in data.index:
            func(i, data)
        logging.debug(f'HistoricalRunner started')

    def stop(self) -> NoReturn:
        """ Stop the Runner """
        self.is_running = False
        logging.debug(f'HistoricalRunner stopped')
