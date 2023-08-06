from __future__ import annotations
from abc import abstractmethod
from typing import Union
from . import HasContext


class Performance(HasContext):
    timestamp = 0
    duration = 0

    def __init__(self):
        self.duration = 0
        self.duration = 0
        HasContext.__init__(self)

    # Start the timer.
    # type: None|float
    # param: timestamp
    # return: Performance
    @abstractmethod
    def start(self, timestamp=None) -> Performance:
        self.timestamp = timestamp if timestamp is not None else self.get_microtime()
        return self

    # Stop the timer and calculate duration.
    # type: None|float
    # param: duration
    # return: Performance
    @abstractmethod
    def end(self, duration: Union[None, float] = 0) -> Performance:
        """
        :type: object
        """
        self.duration = duration if duration else (self.get_microtime() - self.timestamp)
        self.duration = float(round(self.duration, 4))
        return self

    def get_timestamp(self):
        return self.timestamp

    def get_duration(self):
        return self.duration
