import os
import logging.handlers
import unittest
from meerkat import FakeMonitor
from unittest.mock import *


class FakeMonitorTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_monitor_info_return_correct_info(self):
        monitor = FakeMonitor()
        self.assertEqual("Monitor를 간단하게 구현한 Fake 객체입니다.", monitor.get_monitor_info())

    def test_get_data_return_correct_data(self):
        monitor = FakeMonitor()
        self.assertEqual("1번째 데이터 입니다", monitor.get_data())
        self.assertEqual("2번째 데이터 입니다", monitor.get_data())
        self.assertEqual("3번째 데이터 입니다", monitor.get_data())

    def test_get_heartbeat_return_correct_data(self):
        monitor = FakeMonitor()
        hb = monitor.get_heartbeat()
        self.assertEqual(True, hb["ok"])
        self.assertEqual("정상적으로 모니터링 되고 있습니다", hb["message"])

    def test_set_config_set_correctly(self):
        monitor = FakeMonitor()
        self.assertEqual("A", monitor.type)
        monitor.set_config({"type": "B"})
        self.assertEqual("B", monitor.type)
        monitor.set_config({"type": "D"})
        self.assertEqual("B", monitor.type)

    def test_get_config_info_return_correct_data(self):
        monitor = FakeMonitor()
        self.assertEqual(
            "type을 A, B, C 중 하나로 설정 할 수 있습니다. 예. {'type': 'A' }", monitor.get_config_info()
        )
