from .. import Arrayable
from typing import Union
import resource
import socket
import platform

class HOST(Arrayable):
    hostname: Union[str, None] = None
    ip: Union[str, None] = None
    os: Union[str, None] = None
    url: Union[str, None] = None
    cpu: Union[float, None] = None
    ram: Union[float, None] = None
    hdd: Union[str, None] = None

    def __init__(self):
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(socket.gethostname())
        self.cpu = 0
        self.with_server_status()
        self.set_os(platform.version())

    def with_server_status(self):
        ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.set_ram(ram)

    def set_hostname(self, hostname: str) -> None:
        self.hostname = hostname

    def set_ip(self, ip: str) -> None:
        self.ip = ip

    def set_os(self, os: str) -> None:
        self.os = os

    def set_cpu(self, cpu: float) -> None:
        self.cpu = cpu

    def set_ram(self, ram: float) -> None:
        self.ram = ram

    def set_hdd(self, hdd: str) -> None:
        self.hdd = hdd

    def get_hostname(self) -> str:
        return self.hostname

    def get_url(self) -> str:
        return self.url

    def get_cpu(self) -> float:
        return self.cpu

    def get_ram(self) -> float:
        return self.ram

    def get_hdd(self) -> str:
        return self.hdd
