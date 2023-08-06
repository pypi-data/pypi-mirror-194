from ..inspector import Configuration, Inspector
from ..inspector.models import Segment
import unittest


class TestAgent(unittest.TestCase):
    inspector = None

    def setUp(self):
        configuration = Configuration('example-api-key')
        configuration.set_enabled(False)
        self.inspector = Inspector(configuration)
        self.inspector.start_transaction('transaction-test')

    def test_inspector_instance(self):
        self.assertIsInstance(self.inspector, Inspector, msg=None)

    def test_add_entry(self):
        obj = self.inspector.add_entries(self.inspector.start_segment('segment-test'))
        self.assertIsInstance(obj, Inspector, msg=None)
        obj = self.inspector.add_entries([self.inspector.start_segment('segment-test')])
        self.assertIsInstance(obj, Inspector, msg=None)

    def test_add_segment(self):
        segment = self.inspector.start_segment('process', 'test segment')
        self.assertIsInstance(segment, Segment, msg=None)

    def test_add_segment_with_context(self):
        text = 'test_segment'
        self.inspector.start_segment('process', text)
        context_test = {
            'foo_segment': 'bar'
        }
        self.inspector.segment().add_context(text, context_test)
        context_test = {
            text: context_test
        }
        self.assertEquals(context_test, self.inspector.segment().context)

    def test_status_check(self):
        self.assertFalse(self.inspector.is_recording())
        self.assertFalse(self.inspector.need_transaction())
        self.assertFalse(self.inspector.can_add_segments())

        self.assertIsInstance(self.inspector.start_recording(), Inspector)
        self.assertTrue(self.inspector.is_recording())
        self.assertTrue(self.inspector.can_add_segments())

