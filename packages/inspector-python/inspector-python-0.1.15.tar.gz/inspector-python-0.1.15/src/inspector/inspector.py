from __future__ import annotations
from . import Configuration
from .models.enums import TransportType
from .models import Transaction, Segment, Error
from .models.enums import TransactionType, ModelType

# import http.client
# import multiprocessing
from.transports import SyncTransport, AsyncTransport


class Inspector:
    # Agent configuration.
    # type: Configuration
    _configuration: Configuration = None

    # Transport strategy.
    # type:
    _transport = None

    # Current transaction.
    # type:
    _transaction = None

    # Current Segment.
    # type:
    _segment = None

    # Current Error.
    # type:
    _error = None

    # Runa callback before flushing data to the remote platform.
    # type:
    _beforeCallbacks = []

    def __init__(self, configuration: Configuration):
        self._configuration = configuration
        if configuration.get_transport() == TransportType.ASYNC.value:
            self._transport = AsyncTransport(configuration)
        else:
            self._transport = SyncTransport(configuration)
            self._transport.set_format_send(False)

    def __del__(self):
        self.flush()

    def set_transport(self, resolver):
        pass

    def start_transaction(self, name, type_str=TransactionType.PROCESS.value):
        self._transaction = Transaction(name, type_str)
        self._transaction.start()
        self.add_entries(self._transaction)
        return self._transaction

    # Get current transaction instance.
    # return null|Transaction
    def transaction(self) -> Transaction:
        return self._transaction

    # Get current segment instance.
    # return null|Segment
    def segment(self) -> Segment:
        return self._segment

    # Determine if an active transaction exists.
    # return: bool
    def has_transaction(self) -> bool:
        return True if self._transaction else False

    # Determine if the current cycle hasn't started its transaction yet.
    # return: bool
    def need_transaction(self) -> bool:
        return self.is_recording() and not self.has_transaction()

    # Determine if a new segment can be added.
    # return: bool
    def can_add_segments(self) -> bool:
        return self.is_recording() and self.has_transaction()

    # Check if the monitoring is enabled.
    # return: bool
    def is_recording(self) -> bool:
        return self._configuration.is_enabled()

    # Enable recording.
    # return: Inspector
    def start_recording(self) -> Inspector:
        self._configuration.set_enabled(True)
        return self

    # Disable recording.
    # return: Inspector
    def stop_recording(self) -> Inspector:
        self._configuration.set_enabled(False)
        return self

    def start_segment(self, type_str=TransactionType.PROCESS.value, label=None) -> Segment:
        self._segment = Segment(self._transaction, type_str, label)
        self._segment.start()
        self.add_entries(self._segment)
        return self._segment

    def add_segment(self, callback, type_str, label=None, throw=False):
        self.start_segment(type_str, label)
        result = callback()
        self.segment().end()
        return result

    def report_exception(self, exception, handled=True):
        if self.need_transaction():
            self.start_transaction(exception.__class__.__name__)

        segment = self.start_segment(ModelType.EXCEPTION.value, str(exception))

        error = (Error(exception, self._transaction)).set_handled(handled)
        self.add_entries(error)
        segment.add_context('Error', error).end()
        return error

    def add_entries(self, entries) -> Inspector:
        if isinstance(entries, Transaction):
            self._transaction = self._transport.add_entry(entries)
        elif isinstance(entries, Segment):
            self._segment = self._transport.add_entry(entries)
        elif isinstance(entries, Error):
            self._error = self._transport.add_entry(entries)
        return self

    @staticmethod
    def before_flush(self, callback):
        pass

    def flush(self):
        if not self.is_recording() or not self.has_transaction():
            return
        self.transaction().end()
        self._transport.flush()
        del self._transaction
        if self._segment is not None:
            del self._segment
        if self._error is not None:
            del self._error
