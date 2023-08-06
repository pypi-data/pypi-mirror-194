from __future__ import annotations
from typing import Union, Any
from . import Performance
from .partials import HOST, User, HTTP
import random
import string
from .enums import TransactionType, ModelType
import resource
import json


class Transaction(Performance):
    TYPE_REQUEST = TransactionType.REQUEST.value
    TYPE_PROCESS = TransactionType.PROCESS.value

    name: Union[str, None] = None
    model: Union[str, None] = None
    type: Union[str, None] = None
    hash: Union[str, None] = None
    host: Union[str, HOST, None] = None
    http: Union[str, HTTP, None] = None
    user: Union[str, None] = None
    result: Union[str, None] = None
    user: Union[User, None] = None
    memory_peak: Union[float, None] = 0
    # duration = 0
    context: list = []
    # context: dict = {}
    cookies: list = []
    headers: list = []

    def __init__(self, name: str, type_str: Union[str, None] = None) -> None:
        Performance.__init__(self)
        self.model = ModelType.TRANSACTION.value
        self.name = name
        self.type = type_str
        self.memory_peak = 0
        self.result = ""
        self.context = {}
        self.hash = self.__generate_unique_hash()
        # self.duration = 0
        self.host = HOST()
        if self.type == self.TYPE_REQUEST:
            self.http = HTTP()

    def set_host(self, host_data: HOST) -> Transaction:
        self.host = host_data
        return self

    def set_http(self, http_data: HTTP) -> Transaction:
        self.http = http_data
        return self

    def add_context(self, label: Union[str, int], data: Any) -> Transaction:
        self.context[label] = data
        return self

    def with_user(self, id: str, name: Union[str, None] = None, email: Union[str, None] = None) -> Transaction:
        self.user = User(id=id, name=name, email=email)
        return self

    def get_json(self) -> str:
        return json.loads(
            json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        )

    def end(self, duration: Union[float, None] = None):
        self.memory_peak = self.get_memory_peak()
        obj = Performance.end(self, duration)
        return obj

    def get_memory_peak(self):
        return round((resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024), 2)

    def sample_server_status(self, ratio: float):
        pass

    def set_result(self, result: str) -> Transaction:
        self.result = result
        return self

    def is_ended(self) -> bool:
        return self.duration is not None and self.duration > 0

    def __generate_unique_hash(self, length: int = 32) -> str:
        """
        Generate a unique transaction hash.
        :param length: length hash, default 32
        :type length: int
        :return: str
        """
        if length is None or length < 32:
            length = 32
        hash_str = ''.join(random.sample(string.ascii_letters + string.digits, length))
        return hash_str
