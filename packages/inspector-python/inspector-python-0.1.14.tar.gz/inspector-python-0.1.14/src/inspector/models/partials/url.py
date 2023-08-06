from .. import Arrayable
from typing import Union


class URL(Arrayable):
    protocol: Union[str, None] = None
    port: int = 80
    path: Union[str, None] = None
    search: Union[str, None] = None
    full: Union[str, None] = None

    def __init__(self):
        self.protocol = ""
        self.port = 0
        self.path = ""
        self.search = ""
        self.full = ""

    def set_protocol(self, protocol: str) -> None:
        self.protocol = protocol

    def set_port(self, port: int) -> None:
        self.port = port

    def set_path(self, path: str) -> None:
        self.path = path

    def set_search(self, search: str) -> None:
        self.search = search

    def set_full(self, full: str) -> None:
        self.full = full

    def get_protocol(self) -> str:
        return self.protocol

    def get_port(self) -> int:
        return self.port

    def get_path(self) -> str:
        return self.path

    def get_search(self) -> str:
        return self.search

    def get_full(self) -> str:
        return self.full
