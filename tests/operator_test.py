import time
import unittest
from meerkat import Operator, FakeMonitor
from unittest.mock import *

class OperatorTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_set_alarm_listener_should_set_alarm_cb(self):
        """Test set_alarm_listener() should set alarm_cb"""

        operator = Operator()
        operator.set_alarm_listener("alarm_cb")
        self.assertEqual("alarm_cb", operator.alarm_cb)

    def test_register_monitor_should_register_monitor(self):
        """Test register_monitor() should register monitor"""

        operator = Operator()
        monitor = FakeMonitor()
        monitor.CODE = "mango"
        operator.register_monitor(monitor)
        self.assertEqual(operator.monitor["mango"], monitor)

    def test_unregister_monitor_should_unregister_monitor(self):
        """Test unregister_monitor() should unregister monitor"""

        operator = Operator()
        monitor = FakeMonitor()
        monitor.CODE = "mango"
        operator.register_monitor(monitor)
        operator.unregister_monitor("mango")
        self.assertEqual("mango" not in operator.monitor, True)

    def test_get_monitor_list_should_return_monitor_list(self):
        """Test get_monitor_list() should return monitor list"""

        operator = Operator()
        monitor = FakeMonitor()
        monitor.CODE = "mango"
        operator.register_monitor(monitor)
        monitor2 = FakeMonitor()
        monitor2.CODE = "orange"
        operator.register_monitor(monitor2)
        self.assertEqual(operator.get_monitor_list(), ["mango", "orange"])

    def test_get_analysis_result_should_return_analyzer(self):
        """Test get_analysis_result() should return analyzer"""

        operator = Operator()
        monitor = FakeMonitor()
        monitor.CODE = "mango"
        operator.register_monitor(monitor)
        self.assertEqual(operator.get_analysis_result("mango"), {'message': 'Fake Monitor Analysis', 'image_file': None})

    def test_get_analysis_result_should_return_none_when_monitor_not_exist(self):
        """Test get_analysis_result() should return None when monitor not exist"""

        operator = Operator()
        self.assertEqual(operator.get_analysis_result("mango"), None)

    def test_set_alarm_should_call_set_alarm_of_all_registered_monitor(self):
        """Test set_alarm() should call set_alarm() of all registered monitor"""

        operator = Operator()
        monitor = FakeMonitor()
        monitor.CODE = "mango"
        monitor.set_alarm = MagicMock()
        operator.register_monitor(monitor)
        operator.set_alarm("mango", True)
        monitor.set_alarm.assert_called_with(True)

        operator.set_alarm("mango", False)
        monitor.set_alarm.assert_called_with(False)

    def test_set_alarm_should_not_call_set_alarm_when_monitor_not_exist(self):
        """Test set_alarm() should not call set_alarm() when monitor not exist"""

        operator = Operator()
        monitor = FakeMonitor()
        monitor.CODE = "mango"
        monitor.set_alarm = MagicMock()
        operator.register_monitor(monitor)
        operator.set_alarm("orange", True)
        monitor.set_alarm.assert_not_called()


class OperatorStartStopTests(unittest.TestCase):
    def test_start_should_call_worker_start_and_post_first_task(self):
        """Test start() should call worker.start() and post first task"""

        operator = Operator()
        operator.worker = MagicMock()
        operator.start()
        operator.worker.start.assert_called()
        operator.worker.post_task.assert_called()
        operator.stop()

    def test_start_should_not_call_worker_start_when_already_running(self):
        """Test start() should not call worker.start() when already running"""

        operator = Operator()
        operator.worker = MagicMock()
        operator.is_running = True
        operator.start()
        operator.worker.start.assert_not_called()
        operator.worker.post_task.assert_not_called()
        operator.stop()

    def test_start_should_call_monitor_do_check_and_alarm_cb_with_correct_msg(self):
        """Test start() should call monitor.do_check() and alarm_cb with correct msg"""

        operator = Operator()
        monitor_mock = FakeMonitor()
        monitor_mock.do_check = AsyncMock(
            return_value={
                "ok": True,
                "alarm": {
                    "message": "alert_orange",
                },
            }
        )
        alarm_listener_mock = MagicMock()
        operator.set_alarm_listener(alarm_listener_mock)
        operator.register_monitor(monitor_mock)
        operator.interval = 1
        self.assertFalse(monitor_mock.do_check.called)
        operator.start()
        self.assertTrue(operator.is_running)

        time.sleep(1)
        self.assertTrue(monitor_mock.do_check.called)
        alarm_listener_mock.assert_called()
        self.assertEqual(1, len(monitor_mock.do_check.call_args_list))
        self.assertEqual(1, len(alarm_listener_mock.call_args_list))

        time.sleep(1)
        self.assertEqual(2, len(monitor_mock.do_check.call_args_list))
        self.assertEqual(2, len(alarm_listener_mock.call_args_list))

        time.sleep(1)
        self.assertEqual(3, len(monitor_mock.do_check.call_args_list))
        self.assertEqual(3, len(alarm_listener_mock.call_args_list))
        operator.stop()

        time.sleep(1)
        self.assertFalse(operator.is_running)

    def test_start_should_call_alarm_cb_when_None_result_is_returned(self):
        """Test start() should call alarm_cb when None result is returned"""

        operator = Operator()
        monitor_mock = FakeMonitor()
        monitor_mock.do_check = AsyncMock(return_value=None)
        alarm_listener_mock = MagicMock()
        operator.set_alarm_listener(alarm_listener_mock)
        operator.register_monitor(monitor_mock)
        operator.interval = 1
        self.assertFalse(monitor_mock.do_check.called)
        operator.start()
        self.assertTrue(operator.is_running)

        time.sleep(1)
        self.assertTrue(monitor_mock.do_check.called)
        alarm_listener_mock.assert_called()
        self.assertEqual(1, len(monitor_mock.do_check.call_args_list))
        self.assertEqual(1, len(alarm_listener_mock.call_args_list))

        time.sleep(1)
        self.assertEqual(2, len(monitor_mock.do_check.call_args_list))
        self.assertEqual(2, len(alarm_listener_mock.call_args_list))

        time.sleep(1)
        self.assertEqual(3, len(monitor_mock.do_check.call_args_list))
        self.assertEqual(3, len(alarm_listener_mock.call_args_list))
        operator.stop()

        time.sleep(1)
        self.assertFalse(operator.is_running)

    def test_stop_should_not_call_monitor_do_check_and_alarm_cb_when_after_stop(self):
        """Test stop() should not call monitor.do_check() and alarm_cb when after stop"""

        operator = Operator()
        monitor_mock = FakeMonitor()
        monitor_mock.do_check = AsyncMock(
            return_value={
                "ok": True,
                "alarm": {
                    "message": "alert_orange",
                },
            }
        )
        alarm_listener_mock = MagicMock()
        operator.set_alarm_listener(alarm_listener_mock)
        operator.register_monitor(monitor_mock)
        operator.interval = 1
        self.assertFalse(monitor_mock.do_check.called)
        operator.start()
        self.assertTrue(operator.is_running)

        time.sleep(1)
        self.assertTrue(monitor_mock.do_check.called)
        alarm_listener_mock.assert_called()
        self.assertEqual(1, len(monitor_mock.do_check.call_args_list))
        self.assertEqual(1, len(alarm_listener_mock.call_args_list))

        operator.stop()
        time.sleep(1)
        self.assertFalse(operator.is_running)
        self.assertTrue(3 > len(monitor_mock.do_check.call_args_list))
        self.assertTrue(3 > len(alarm_listener_mock.call_args_list))

        time.sleep(1)
        self.assertTrue(3 > len(monitor_mock.do_check.call_args_list))
        self.assertTrue(3 > len(alarm_listener_mock.call_args_list))

        time.sleep(1)


class OperatorHeartbeatTests(unittest.TestCase):
    def test_get_heartbeat_should_call_monitor_get_heartbeat_and_alarm_cb_with_correct_msg(self):
        """Test get_heartbeat() should call monitor.get_heartbeat() and alarm_cb with correct msg"""

        operator = Operator()
        monitor_mock = FakeMonitor()
        monitor_mock.get_heartbeat = AsyncMock(
            return_value={
                "ok": True,
                "message": "heartbeat_orange",
            }
        )
        monitor_mock.do_check = AsyncMock(return_value=None)
        alarm_listener_mock = MagicMock()
        operator.set_alarm_listener(alarm_listener_mock)
        operator.register_monitor(monitor_mock)
        operator.interval = 1
        operator.start()
        self.assertFalse(monitor_mock.get_heartbeat.called)
        operator.get_heartbeat()

        time.sleep(1)
        self.assertTrue(monitor_mock.get_heartbeat.called)
        alarm_listener_mock.assert_called()
        self.assertEqual(1, len(monitor_mock.get_heartbeat.call_args_list))

        time.sleep(1)
        self.assertEqual(1, len(monitor_mock.get_heartbeat.call_args_list))
        operator.stop()

    def test_get_heartbeat_should_not_call_get_heartbeat_when_not_started(self):
        """Test get_heartbeat() should not call get_heartbeat() when not started"""

        operator = Operator()
        monitor_mock = FakeMonitor()
        monitor_mock.get_heartbeat = AsyncMock(
            return_value={
                "ok": True,
                "message": "heartbeat_orange",
            }
        )
        monitor_mock.do_check = AsyncMock(return_value=None)
        alarm_listener_mock = MagicMock()
        operator.set_alarm_listener(alarm_listener_mock)
        operator.register_monitor(monitor_mock)
        operator.interval = 1
        self.assertFalse(monitor_mock.get_heartbeat.called)
        operator.get_heartbeat()
        self.assertFalse(monitor_mock.get_heartbeat.called)

    def test_get_heartbeat_should_not_call_get_heartbeat_when_monitor_is_not_registered(self):
        """Test get_heartbeat() should not call get_heartbeat() when monitor is not registered"""

        operator = Operator()
        monitor_mock = FakeMonitor()
        monitor_mock.get_heartbeat = AsyncMock(
            return_value={
                "ok": True,
                "message": "heartbeat_orange",
            }
        )
        monitor_mock.do_check = AsyncMock(return_value=None)
        alarm_listener_mock = MagicMock()
        operator.set_alarm_listener(alarm_listener_mock)
        operator.interval = 1
        operator.start()
        self.assertFalse(monitor_mock.get_heartbeat.called)
        operator.get_heartbeat()
        self.assertFalse(monitor_mock.get_heartbeat.called)
