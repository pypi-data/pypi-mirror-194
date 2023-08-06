from abc import ABC
from ..models import Arrayable


class TransportInterface(ABC):

    # Add an Arrayable entity in the queue.
    # param: entry
    # type: Arrayable
    def add_entry(self, entry: Arrayable):
        pass

    # Send data to Inspector.
    # This method is invoked after your application has sent
    # the response to the client.
    # So this is the right place to perform the data transfer.
    # return: mixed
    def flush(self):
        pass
