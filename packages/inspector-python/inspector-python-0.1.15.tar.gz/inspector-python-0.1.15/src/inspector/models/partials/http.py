from .. import Arrayable
from . import URL

class HTTP(Arrayable):
    request = None
    url: URL = None

    def __init__(self):
        # self.request = RequestInspector()
        self.url = URL()

    def set_request(self, request) -> None:
        self.request = request

    def set_url(self, url: URL) -> None:
        self.url = url

    def get_request(self):
        return self.request

    def get_url(self) -> URL:
        return self.url
