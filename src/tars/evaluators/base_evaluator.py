from collections import namedtuple
import pandas as pd


class BaseEvaluator:

    def __init__(self):
        self.checkpoints = {}

    def add_checkpoint(self, dtime, value):
        self.checkpoints[dtime] = [value]

    def evaluate(self):
        df = pd.DataFrame.from_dict(self.checkpoints, orient='index')
        return df
