from enum import Enum


class ModelType(Enum):
    TRANSACTION: str = 'transaction'
    SEGMENT: str = 'segment'
    ERROR: str = 'error'
    EXCEPTION: str = 'exception'
