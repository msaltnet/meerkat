import unittest
from meerkat import Operator
from unittest.mock import *


class OperatorTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_monitor_info_return_correct_info(self):
        operator = Operator()
        operator.initialize("mango", "orange", "handler")
        self.assertEqual("mango", operator.monitor)
        self.assertEqual("orange", operator.reporter)
        self.assertEqual("handler", operator.alarm_handler)
        self.assertEqual(None, operator.analyzer)

        operator.initialize("mango", "orange", "handler", "apple")
        self.assertEqual("apple", operator.analyzer)
