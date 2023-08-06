from __future__ import annotations
from typing import Union, Any
import json
import time
from abc import abstractmethod


class HasContext:
    context: Union[None, dict] = {}

    # Add contextual information.
    # param: label
    # type: str|int
    # param: data
    # type: Any
    # return: HasContext
    @abstractmethod
    def add_context(self, label: Union[str, int], data: Any) -> HasContext:
        self.context[label] = data
        return self

    # Set contextual information.
    # param: context
    # type: dict
    # return: HasContext
    @abstractmethod
    def set_context(self, context: dict) -> HasContext:
        self.context = context
        return self

    # Get contextual information.
    # param: label
    # type: None|str|int
    # return: Any
    @abstractmethod
    def get_context(self, label: Union[None, str, int] = None) -> Any:
        if label:
            if label in self.context:
                return self.context[label]
            else:
                return None
        return self.context

    # Convert the object to json recursively
    # return: str
    @abstractmethod
    def get_json(self) -> str:
        return json.loads(
            json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)), indent=100)
        )

    def get_microtime(self):
        time_value = float(time.time())
        return (round(time_value, 4))
