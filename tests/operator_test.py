import time
import unittest
from meerkat import Operator
from unittest.mock import *


class OperatorTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_monitor_info_return_correct_info(self):
        """Test get_monitor_info() return correct info"""

        operator = Operator()
        operator.initialize("mango", "orange", "handler", "apple")
        self.assertEqual("mango", operator.monitor)
        self.assertEqual("orange", operator.reporter)
        self.assertEqual("handler", operator.alarm_handler)
        self.assertEqual("apple", operator.analyzer)

    def test_start_should_call_monitor_get_info_and_report_get_report_message(self):
        """Test start() should call monitor.get_info() and report.get_report_message()"""

        operator = Operator()
        monitor_mock = MagicMock()
        monitor_mock.get_info = MagicMock(return_value="banana")
        reporter_mock = MagicMock()
        reporter_mock.get_report_message = MagicMock(return_value=None)
        analyzer_mock = MagicMock()
        analyzer_mock.put_info = MagicMock()
        alarm_handler = MagicMock()
        operator.interval = 1
        operator.initialize(monitor_mock, reporter_mock, alarm_handler, analyzer_mock)
        operator.start()
        self.assertTrue(operator.is_running)

        time.sleep(1)
        monitor_mock.get_info.assert_called()
        analyzer_mock.put_info.assert_called_with("banana")
        reporter_mock.get_report_message.assert_called_with("banana")
        alarm_handler.assert_not_called()
        self.assertEqual(1, len(monitor_mock.get_info.call_args_list))
        self.assertEqual(1, len(reporter_mock.get_report_message.call_args_list))
        self.assertEqual(1, len(analyzer_mock.put_info.call_args_list))

        time.sleep(1)
        self.assertEqual(2, len(monitor_mock.get_info.call_args_list))
        self.assertEqual(2, len(reporter_mock.get_report_message.call_args_list))
        self.assertEqual(2, len(analyzer_mock.put_info.call_args_list))

        time.sleep(1)
        self.assertEqual(3, len(monitor_mock.get_info.call_args_list))
        self.assertEqual(3, len(reporter_mock.get_report_message.call_args_list))
        self.assertEqual(3, len(analyzer_mock.put_info.call_args_list))
        operator.stop()
        time.sleep(1)
        self.assertFalse(operator.is_running)

    def test_start_should_call_alarm_handler_when_not_None_result_is_returned(self):
        """Test start() should call alarm_handler when not None result is returned"""

        operator = Operator()
        monitor_mock = MagicMock()
        monitor_mock.get_info = MagicMock(return_value="banana")
        reporter_mock = MagicMock()
        reporter_mock.get_report_message = MagicMock(return_value="alert_orange")
        analyzer_mock = MagicMock()
        analyzer_mock.put_info = MagicMock()
        alarm_handler = MagicMock()
        operator.interval = 1
        operator.initialize(monitor_mock, reporter_mock, alarm_handler, analyzer_mock)
        operator.start()
        self.assertTrue(operator.is_running)

        time.sleep(1)
        monitor_mock.get_info.assert_called()
        analyzer_mock.put_info.assert_called_with("alert_orange")
        reporter_mock.get_report_message.assert_called_with("banana")
        alarm_handler.assert_called_with("alert_orange")

        self.assertEqual(1, len(monitor_mock.get_info.call_args_list))
        self.assertEqual(1, len(reporter_mock.get_report_message.call_args_list))
        self.assertEqual(2, len(analyzer_mock.put_info.call_args_list))

        time.sleep(1)
        self.assertEqual(2, len(monitor_mock.get_info.call_args_list))
        self.assertEqual(2, len(reporter_mock.get_report_message.call_args_list))
        self.assertEqual(4, len(analyzer_mock.put_info.call_args_list))

        time.sleep(1)
        self.assertEqual(3, len(monitor_mock.get_info.call_args_list))
        self.assertEqual(3, len(reporter_mock.get_report_message.call_args_list))
        self.assertEqual(6, len(analyzer_mock.put_info.call_args_list))
        operator.stop()
        time.sleep(1)
        self.assertFalse(operator.is_running)

    def test_get_heartbeat_should_return_heartbeat_state(self):
        """Test get_heartbeat() should return heartbeat_state"""

        mock_monitor = MagicMock()
        mock_monitor.get_heartbeat = MagicMock(return_value="mango")
        operator = Operator()
        operator.initialize(mock_monitor, "orange", "handler", "apple")
        self.assertEqual("mango", operator.get_heartbeat())
        mock_monitor.get_heartbeat.assert_called()

    def test_get_heartbeat_should_return_False_when_operator_is_NOT_initialized(self):
        """Test get_heartbeat() should return False when operator is NOT initialized"""

        operator = Operator()
        self.assertFalse(operator.get_heartbeat())

    def test_get_config_info_should_return_config_info_of_monitor_when_monitor_config_True(self):
        """Test get_config_info() should return config_info when monitor.config is True"""

        mock_monitor = MagicMock()
        mock_monitor.get_config_info = MagicMock(return_value="mango")
        mock_reporter = MagicMock()
        mock_reporter.get_config_info = MagicMock(return_value="orange")
        operator = Operator()
        operator.initialize(mock_monitor, mock_reporter, "handler", "apple")
        self.assertEqual("mango", operator.get_config_info(monitor_config=True))
        mock_monitor.get_config_info.assert_called()
        mock_reporter.get_config_info.assert_not_called()

    def test_get_config_info_should_return_config_info_of_reporter_when_monitor_config_False(self):
        """Test get_config_info() should return config_info when monitor.config is False"""

        mock_monitor = MagicMock()
        mock_monitor.get_config_info = MagicMock(return_value="mango")
        mock_reporter = MagicMock()
        mock_reporter.get_config_info = MagicMock(return_value="orange")
        operator = Operator()
        operator.initialize(mock_monitor, mock_reporter, "handler", "apple")
        self.assertEqual("orange", operator.get_config_info(monitor_config=False))
        mock_monitor.get_config_info.assert_not_called()
        mock_reporter.get_config_info.assert_called()

    def test_get_config_info_should_return_invalid_state_when_operator_is_NOT_initialized(self):
        """Test get_config_info() should return False when operator is NOT initialized"""

        operator = Operator()
        self.assertEqual("invalid monitor", operator.get_config_info(monitor_config=True))
        self.assertEqual("invalid reporter", operator.get_config_info(monitor_config=False))