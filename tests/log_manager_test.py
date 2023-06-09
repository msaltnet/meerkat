import os
import logging.handlers
import unittest
from meerkat import LogManager
from unittest.mock import *


class LogManagerTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_log_directory_correctly(self):
        """LogManager should create log directory when it is not exist."""

        self.assertTrue(os.path.exists(LogManager.LOG_FOLDER))

    def test_get_logger_return_logger_with_handler(self):
        """Test get_logger() return logger with handler"""

        self.assertEqual("mango" in LogManager.REGISTERED_LOGGER, False)
        logger = LogManager.get_logger("mango")
        self.assertEqual("mango" in LogManager.REGISTERED_LOGGER, True)
        logger2 = LogManager.get_logger("mango")
        self.assertEqual(logger, logger2)

    def test_set_stream_level_call_stream_handler_setLevel(self):
        """Test set_stream_level() call stream handler setLevel()"""

        original = LogManager.STREAM_HANDLER
        LogManager.STREAM_HANDLER = MagicMock()
        LogManager.set_stream_level(50)
        LogManager.STREAM_HANDLER.setLevel.assert_called_once_with(50)
        LogManager.STREAM_HANDLER = original

    def test_change_log_file_should_change_file_handler(self):
        """Test change_log_file() should change file handler"""

        logger = LogManager.get_logger("orange")
        has_RotatingFileHandler = False
        old_handler = None
        for handler in logger.handlers:
            if issubclass(type(handler), logging.handlers.RotatingFileHandler):
                self.assertEqual(handler.baseFilename[-11:], "meerkat.log")
                has_RotatingFileHandler = True
                old_handler = handler
        self.assertTrue(has_RotatingFileHandler)

        has_RotatingFileHandler = False
        LogManager.change_log_file("kiwi.log")
        for handler in logger.handlers:
            if issubclass(type(handler), logging.handlers.RotatingFileHandler):
                self.assertEqual(handler.baseFilename[-8:], "kiwi.log")
                has_RotatingFileHandler = True
                self.assertNotEqual(old_handler, handler)
                old_handler = handler
        self.assertTrue(has_RotatingFileHandler)
