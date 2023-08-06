from abc import abstractmethod
from .. import Configuration
from typing import Union
from . import TransportInterface
from ..models import Transaction, Segment, Error
import tempfile
import base64
import math
import json


class Transport(TransportInterface):
    """
    Key to authenticate remote calls.
    :type _config: Configuration
    """
    _config: Configuration = None

    """
    Custom url of the proxy if needed.
    :type _proxy: str
    """
    _proxy: str = None

    """
    Queue of messages to send.
    :type _queue: list
    """
    _queue: list = []

    __send_base64 = True

    def __init__(self, configuration: Configuration) -> None:
        """
        AbstractApiTransport constructor.
        :type configuration: object
        :raise InspectorException
        """
        self._config = configuration
        # $this->verifyOptions($configuration->getOptions());

    def add_entry(self, item: Union[Transaction, Segment, Error, dict]):
        self._queue.append(item)
        return self._queue[len(self._queue) - 1]

    def flush(self):
        if len(self._queue) <= 0:
            return
        self.send(self._queue)
        self._queue = {}

    def send_via_file(self, data):
        tmpfile = '/'.join([tempfile.mkdtemp(), 'inspector'])
        with open(tmpfile, 'w', encoding='utf-8') as f_out:
            f_out.write(data)
        self._send_chunk(tmpfile)

    def __get_item_json_list(self, items):
        list_data = []
        for item in items:
            list_data.append(item.get_json())
        return list_data

    def send(self, items):
        data = items
        # for item in data:
        #    print('--> ITEM: ', self.__get_item_json_list(item))
        json_data_str = json.dumps(self.__get_item_json_list(items))
        json_length = len(json_data_str)
        count = len(data)
        if json_length > self._config.get_max_post_size():
            if count == 1:
                message_bytes = json_data_str.encode('ascii')
                str_base64 = base64.b64encode(message_bytes)
                return self.send(str_base64)

            chunk_size = math.floor(math.ceil(json_length / self._config.get_max_post_size()))
            chunks = list(self.array_chunks(data, chunk_size))
            for chunk in chunks:
                self.send(chunk)
        else:
            message_bytes = json_data_str.encode('ascii')
            str_base64 = base64.b64encode(message_bytes)
            if self.__send_base64:
                self._send_chunk(str_base64)
            else:
                self._send_chunk(json_data_str)

    def set_format_send(self, base64=True):
        self.__send_base64 = base64

    def _get_allowed_options(self) -> dict:
        allowed_options = {
            'proxy': "/.+/",
            'debug': "/^(0|1)?$/"
        }
        return allowed_options

    def _get_api_headers(self):
        """
        Return header configuration
        :return: list
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Inspector-Key": self._config.get_ingestion_key(),
            "X-Inspector-Version": self._config.get_version()
        }
        return headers

    def array_chunks(self, data, n):
        for i in range(0, n):
            yield data[i::n]

    @abstractmethod
    def _send_chunk(self, data):
        pass
