import unittest
from meerkat import FakeReporter
from unittest.mock import *


class FakeReporterTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_report_message_return_correct_data(self):
        """Test get_report_message() return correct data"""

        report = FakeReporter()
        event_result = report.get_report_message("event data!")
        self.assertEqual(True, event_result["alarm"])
        self.assertEqual("Data contains events.", event_result["messege"])

        no_event_result = report.get_report_message("even data! even data! even data! even data!")
        self.assertEqual(False, no_event_result["alarm"])
        self.assertEqual("No event", no_event_result["messege"])

    def test_set_config_set_correctly(self):
        """Test set_config() set config correctly"""

        report = FakeReporter()
        self.assertEqual("A", report.type)
        report.set_config({"type": "B"})
        self.assertEqual("B", report.type)
        report.set_config({"type": "D"})
        self.assertEqual("B", report.type)

    def test_get_config_info_return_correct_data(self):
        """Test get_config_info() return correct data"""

        report = FakeReporter()
        self.assertEqual(
            "type을 A, B, C 중 하나로 설정 할 수 있습니다. 예. {'type': 'A' }", report.get_config_info()
        )
