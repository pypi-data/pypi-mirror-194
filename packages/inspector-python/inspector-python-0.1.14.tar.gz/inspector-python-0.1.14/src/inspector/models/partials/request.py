from .. import Arrayable
from typing import Union
from ..partials import Socket


class Request(Arrayable):
    method: Union[str, None] = None
    version: Union[str, None] = None
    cookies: Union[str, None] = None
    headers: list = []
    socket: Socket = None

    def __init__(self):
        self.method = ""
        self.version = ""
        self.cookies = ""
        self.headers = []
        self.socket = Socket()

    def set_method(self, method: str) -> None:
        self.method = method

    def set_version(self, version: str) -> None:
        self.version = version

    def set_cookies(self, cookies: str) -> None:
        self.cookies = cookies

    def set_headers(self, headers: list) -> None:
        self.headers = headers

    def set_socket(self, socket: Socket) -> None:
        self.socket = socket

    def get_method(self) -> str:
        return self.method

    def get_version(self) -> str:
        return self.version

    def get_cookies(self) -> str:
        return self.cookies

    def get_headers(self) -> list:
        return self.headers

    def get_socket(self) -> Socket:
        return self.socket
