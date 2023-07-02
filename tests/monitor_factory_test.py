import unittest
from unittest.mock import *
from meerkat import MonitorFactory, FakeMonitor


class MonitorFactoryTests(unittest.TestCase):
    def test_create_return_None_when_called_with_invalid_code(self):
        monitor = MonitorFactory.create("")
        self.assertEqual(monitor, None)

    def test_create_return_correct_monitor(self):
        self.assertTrue(isinstance(MonitorFactory.create("FMC"), FakeMonitor))

    def test_get_name_return_None_when_called_with_invalid_code(self):
        monitor = MonitorFactory.get_name("")
        self.assertEqual(monitor, None)

    def test_get_name_return_correct_monitor(self):
        self.assertTrue(MonitorFactory.get_name("FMC"), FakeMonitor.NAME)

    def test_get_all_monitor_info_return_correct_info(self):
        all = MonitorFactory.get_all_monitor_info()
        self.assertTrue(all[0]["name"], FakeMonitor.NAME)
        self.assertTrue(all[0]["code"], FakeMonitor.CODE)
        self.assertTrue(all[0]["class"], FakeMonitor)
