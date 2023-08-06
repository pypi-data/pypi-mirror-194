from __future__ import annotations
from . import Performance
from .enums import ModelType
from typing import Union, Any


class Segment(Performance):
    MODEL_NAME = ModelType.SEGMENT.value
    model = None
    label = None
    type = None
    start = None
    context = {}
    transaction = None
    timestamp = None

    def __init__(self, transaction, type, label=None):
        Performance.__init__(self)
        self.model = self.MODEL_NAME
        self.type = type
        self.label = label
        self.context = {}
        self.transaction = transaction
        self.timestamp = self.get_microtime()

    def start(self, timestamp=None) -> Performance:
        initial = self.get_microtime() if timestamp is None else timestamp
        self.start = round((initial - self.transaction.timestamp) * 1000, 4)
        return self

    def add_context(self, label: Union[str, int], data: Any) -> Segment:
        self.context[label] = data
        return self
