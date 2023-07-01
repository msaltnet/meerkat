import unittest
from meerkat import FakeMonitor
from unittest.mock import *
import asyncio


class FakeMonitorTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_do_check_return_correct_info(self):
        """Test do_check() return correct info"""

        monitor = FakeMonitor()
        monitor.set_alarm(True)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(monitor.do_check())
        self.assertEqual({"ok": True, "alarm": {"message": "Fake Monitor Alarm"}}, result)

        monitor.set_alarm(False)
        result = loop.run_until_complete(monitor.do_check())
        self.assertEqual({"ok": True}, result)

    def test_get_heartbeat_return_correct_data(self):
        """Test get_heartbeat() return correct data"""

        monitor = FakeMonitor()
        monitor.set_alarm(True)
        loop = asyncio.get_event_loop()
        hb = loop.run_until_complete(monitor.get_heartbeat())
        self.assertTrue(hb["ok"])
        self.assertEqual("정상적으로 모니터링 되고 있습니다. 알림이 켜져 있습니다", hb["message"])
        monitor.set_alarm(False)
        hb = loop.run_until_complete(monitor.get_heartbeat())
        self.assertFalse(hb["ok"])
        self.assertEqual("정상적으로 모니터링 되고 있습니다. 알림이 꺼져 있습니다", hb["message"])

    def test_set_alarm_set_correctly(self):
        """Test set_alarm() set correctly"""

        monitor = FakeMonitor()
        monitor.set_alarm(True)
        self.assertTrue(monitor.alarm_on)
        monitor.set_alarm(False)
        self.assertFalse(monitor.alarm_on)

    def test_get_analysis_return_correct_analysis_data(self):
        """Test get_analysis() return correct analysis data"""

        monitor = FakeMonitor()
        self.assertEqual(
            {"message": "Fake Monitor Analysis", "image_file": None},
            monitor.get_analysis(),
        )
