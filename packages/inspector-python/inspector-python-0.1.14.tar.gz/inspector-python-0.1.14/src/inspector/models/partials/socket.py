from .. import Arrayable
from typing import Union


class Socket(Arrayable):
    remote_address: Union[str, None] = None
    encrypted: bool = None

    def __init__(self):
        self.remote_address = ""
        self.encrypted = False

    def set_remote_address(self, remote_address: str) -> None:
        self.remote_address = remote_address

    def set_encrypted(self, encrypted: bool) -> None:
        self.encrypted = encrypted

    def get_remote_address(self) -> str:
        return self.remote_address

    def get_encrypted(self) -> bool:
        return self.encrypted
