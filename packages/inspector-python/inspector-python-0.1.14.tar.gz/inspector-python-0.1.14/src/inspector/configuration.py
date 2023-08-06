from __future__ import annotations
import platform
from .models.enums import TransportType


class Configuration:
    # Remote endpoint to send data.
    # type: str
    _url = "ingest.inspector.dev"

    # Authentication key.
    # type: str
    _ingestion_key = None

    # type: bool
    _enabled = True

    # Max numbers of items to collect in a single session.
    # type: int
    _max_items = 100

    # type: TransportType
    _transport: TransportType = TransportType.ASYNC

    # type: int
    _server_sampling_ratio = 0

    # type: str
    _version = '3.7.16'

    # type: list
    _options = []

    # Value max size of a POST request content for Windows.
    # type: int
    __post_size_windows = 8000

    # Value max size of a POST request content for Linux.
    # type: int
    __post_size_linux = 65536

    # Environment constructor.
    # param: ingestion_key
    # type: str|None
    # raise: ValueError
    def __init__(self, ingestion_key=None):
        if ingestion_key:
            self.set_ingestion_key(ingestion_key)

    # Verify if api key is well formed.
    # param: ingestion_key
    # type: str
    # return: Configuration
    # raise: ValueError
    def set_ingestion_key(self, ingestion_key: str) -> Configuration:
        ingestion_key = ingestion_key.strip()
        if not ingestion_key:
            raise ValueError('Ingestion key cannot be empty')
        self._ingestion_key = ingestion_key
        return self

    # Get current API key.
    # return: str
    def get_ingestion_key(self) -> str:
        return self._ingestion_key

    # Value max size of a POST request content for Windows.
    # return: int
    def get_max_post_size(self) -> int:
        return self.__post_size_windows if platform.system() == 'Windows' else self.__post_size_linux

    # Max numbers of items to collect in a single session.
    # return: int
    def get_max_items(self) -> int:
        return self._max_items

    # Set max numbers of items to collect in a single session.
    # param: max_items
    # type: str
    # return: Configuration
    # raise: ValueError
    def set_max_items(self, max_items: int) -> Configuration:
        if max_items < 1:
            raise ValueError('Max items it must be greater than 0')
        self._max_items = max_items
        return self

    # Get ingestion endpoint.
    # return: str
    def get_url(self) -> str:
        return self._url

    # Set ingestion endpoint.
    # param: url
    # type: str
    # return: Configuration
    # raise: ValueError
    def set_url(self, url: str) -> Configuration:
        url = url.strip()
        if not url:
            raise ValueError('Url cannot be empty')
        self._url = url
        return self

    def server_sampling_ratio(self, ratio: int = None) -> Configuration | int:
        if not ratio:
            return self._server_sampling_ratio
        self._server_sampling_ratio = ratio

        return self

    # Transport option
    # return: list
    def get_options(self) -> list:
        return self._options

    # Transport option
    # param: key
    # type: str | int
    # return:
    def get_option(self, key: str | int):
        return self._options[key]

    # Add a new entry in the options list.
    # param: key
    # type: str | int
    # param: value
    # return: Configuration
    def set_options(self, key: str | int, value) -> Configuration:
        self._options[key] = value
        return self

    # Get current transport method.
    # return: str
    def get_transport(self) -> str:
        return self._transport

    # Set the preferred transport method.
    # param: transport
    # type: TransportType
    # return: Configuration
    # raise: ValueError
    def set_transport(self, transport: TransportType) -> Configuration:
        if transport not in TransportType._value2member_map_:
            raise ValueError('Transport value not valid')
        self._transport = transport
        return self

    # Set the package version.
    # param: version
    # type: str
    # return: Configuration
    # raise: ValueError
    def set_version(self, version: str) -> Configuration:
        version = version.strip()
        if not version:
            raise ValueError('Version cannot be empty')
        self._version = version
        return self

    # Get the package version.
    # return: str
    def get_version(self) -> str:
        return self._version

    # Enable/Disable data transfer.
    # param: enabled
    # type: bool
    # return: Configuration
    def set_enabled(self, enabled: bool) -> Configuration:
        self._enabled = enabled
        return self

    # Check if data transfer is enabled.
    # return: bool
    def is_enabled(self) -> bool:
        if self._ingestion_key and self._enabled:
            return True
        return False

    # Return data transfer
    # return: bool
    def get_enabled(self) -> bool:
        return self._enabled
