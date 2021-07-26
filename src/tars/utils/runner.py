from typing import ForwardRef
from pandas import Timestamp, Timedelta
from time import sleep


class Runner:
      
    def __init__(self):
        self.is_running = False
    
    def stop(self):
        self.is_running = False

    def start(self, func, frequency, duration=None):
        self.is_running = True

        if duration is not None:
            end_time = Timestamp.now() + Timedelta(duration)
        
        while self.is_running:
            if duration is not None:
                if Timestamp.now() >= end_time:
                    break
            func()
            sleep(Timedelta(frequency).total_seconds())
