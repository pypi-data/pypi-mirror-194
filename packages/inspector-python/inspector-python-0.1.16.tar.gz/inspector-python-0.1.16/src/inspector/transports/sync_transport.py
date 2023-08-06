from . import Transport
from .. import Configuration
import http.client
import ssl


class SyncTransport(Transport):
    PORT = 443
    TIMEOUT = 10

    def __init__(self, configuration: Configuration):
        Transport.__init__(self, configuration)

    def _send_chunk(self, message_bytes):
        headers = self._get_api_headers()
        try:
            connection = http.client.HTTPSConnection(self._config.get_url(), self.PORT, timeout=self.TIMEOUT,
                                                     context=ssl._create_unverified_context())
            connection.request("POST", "/", message_bytes, headers)
            response = connection.getresponse()
            connection.close()
        except Exception as e:
            print('ERROR: ', str(e))
