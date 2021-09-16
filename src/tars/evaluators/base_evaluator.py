from typing import Any, NoReturn
from pandas import Timestamp, DataFrame


class BaseEvaluator:
    """
    The BaseEvaluator is the basic form of Evaluator. It stores data and
    output data.

    :ivar checkpoints: Dict of the data checkpoints
    """

    def __init__(self):
        self.checkpoints = {}

    def add_checkpoint(self, dtime: Timestamp, value: Any) -> NoReturn:
        """ Add a checkpoint

        :param dtime: Pandas Timestamp of the current time
        :param value: Any value to store
        """
        self.checkpoints[dtime] = [value]

    def evaluate(self) -> DataFrame:
        """ Evaluate the stored data

        :return: Pandas DataFrame of the data
        """
        df = DataFrame.from_dict(self.checkpoints, orient='index')
        return df
