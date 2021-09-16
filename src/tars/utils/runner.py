import logging
from typing import Callable, NoReturn
from pandas import Timestamp, Timedelta
from time import sleep


class Runner:
    """
    A Runner represent an object able to execute a function through time.

    The function can be executed with a chosen frequency e.g. every 10 seconds
    and for a optional duration e.g. 2 hours.

    :ivar is_running : Boolean describing if the Runner is running or not.
    """
      
    def __init__(self):
        self.is_running = False

    def start(self, func: Callable, frequency: str, duration: str = None) \
            -> NoReturn:
        """ Start the Runner

        :param func: The function to be executed
        :param frequency: String representing a frequency in the same form than a Pandas' Timedelta (https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html)
        :param duration: String representing a frequency in the same form than a Pandas' Timedelta (https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html)
        """
        self.is_running = True

        if duration is not None:
            end_time = Timestamp.now() + Timedelta(duration)
        
        while self.is_running:
            if duration is not None:
                if Timestamp.now() >= end_time:
                    break
            func()
            sleep(Timedelta(frequency).total_seconds())

        logging.debug(f'Runner started with frequency of {frequency} and '
                      f'duration of {duration}')

    def stop(self) -> NoReturn:
        """ Stop the Runner """
        self.is_running = False
        logging.debug(f'Runner stopped')
