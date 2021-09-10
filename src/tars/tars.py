from threading import Thread
from typing import NoReturn
import sys
import logging

import pandas as pd
from pandas import DataFrame

from utils.runner import Runner


class Tars:
    """
    A trading bot with a name inspired by the movie Interstellar
    """

    def __init__(self, environment='notebook', verbose=True):
        self.strategies = []
        self.runners = []
        self.is_running = False
        self.verbose = verbose
        self.logging = logging
        self.environment = environment
        self._tars = '🤖 TARS'

        if self.verbose:
            logging_level = logging.INFO
        else:
            logging_level = logging.WARNING

        if self.environment == 'server':
            logging.basicConfig(filename='./tars.log',
                                format=' %(asctime)s - %(levelname)s - %(message)s',
                                level=logging_level)
        elif self.environment == 'notebook':
            logging.basicConfig(stream=sys.stdout,
                                format=' %(message)s',
                                level=logging_level)
        else:
            raise Exception('logging location is not recognized')

        logger = logging.getLogger()
        logger.setLevel(logging_level)
        logging.info(f'{self._tars} : Welcome to Endurance! 👨‍🚀')

    def load(self, strategy) -> NoReturn:
        """ Load a strategy to execute """
        self.strategies.append(strategy)
        logging.info(f'{self._tars} : Loaded strategy ➡️ {strategy.name}')

    def start(self, frequency, duration=None) -> NoReturn:
        """
        Start a trading session

        :param frequency: str
            Frequency in the same form than a Pandas' Timedelta
        :param duration: str
            Frequency in the same form than a Pandas' Timedelta
        """
        if self.strategies:
            logging.info(f"{self._tars} : Starting trading session 📈")
            logging.info(f"⏱ Trading decision will be taken every : {frequency}️ (hh:mm:ss)")
            if duration is not None:
                logging.info(f"⏳ for a duration of : {duration} (hh:mm:ss)")
            logging.info(f"💪️ Loading :   ")
            for i, s in enumerate(self.strategies):
                runner = Runner()
                self.runners.append(runner)
                thread = Thread(target=runner.start,
                                args=(s.run, frequency, duration))
                thread.start()
                logging.info(f"  🧵 '{thread.name}' ➡️ '{s.name}'")
            self.is_running = True
        else:
            raise Exception('There are no loaded strategies')

    def plot(self, metric='value') -> NoReturn:
        """ Plot the strategies evolution

        This function shows the evolution of a metric in function of the time
        for the currently running strategies

        :param metric: str
            Must be a metric implemented in utils/metric
        """
        if self.strategies:
            for s in self.strategies:
                series = s.evaluator.evaluate()[metric]
                series.name = s.name
                series.plot(legend=True)
        else:
            raise Exception('There are no loaded strategies')

    def evaluate(self, metric='value', frequency='1min') -> DataFrame:
        """ Displays a table of the strategies evolution

        Shows the raw evolution of a metric through time for all running
        strategies.

        :param metric: str
            Must be a metric implemented in utils/metric
        :param frequency: str
            Displayed frequency can be adjusted given a Pandas Offset

        :return: DataFrame
        """
        if self.strategies:
            metrics = []
            for s in self.strategies:
                series = s.evaluator.evaluate()[metric]
                series.name = s.name
                metrics.append(series)
            df = pd.concat(metrics, axis=1)
            df = df.fillna(method='backfill').resample(frequency).fillna("backfill").round(2)
            return df
        else:
            raise Exception('There are no loaded strategies')

    def stop(self) -> NoReturn:
        """ Stop the trading bot """
        if self.runners:
            for r in self.runners:
                r.stop()
                self.runners.remove(r)
            self.is_running = False
            logging.info(f'{self._tars} : ✋ Stopped all strategies')
