from ..inspector import Configuration, Inspector
from ..inspector.exceptions import InspectorException
from ..inspector.models import Error
import unittest


class TestExceptionEncoder(unittest.TestCase):
    inspector = None

    def setUp(self):
        configuration = Configuration('example-api-key')
        configuration.set_enabled(False)
        self.inspector = Inspector(configuration)
        self.inspector.start_transaction('transaction-test')

    def test_exception_object_result(self):
        code = 1234
        message = 'Test Message'
        try:
            raise InspectorException(message, code)
        except Exception as obj:
            error = Error(obj, self.inspector.transaction())
            self.assertEquals(message, error.message)
            self.assertEquals(__file__, error.file)
            self.assertIsNotNone(error.line)

    def test_empty_exception_message_case(self):
        code = 1234
        message = 'Test Message'
        try:
            raise InspectorException(message, code)
        except Exception as obj:
            error = Error(obj, self.inspector.transaction())
            self.assertEquals(message, error.message)