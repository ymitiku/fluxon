import unittest
import logging
import json
from fluxon.utils import normalize_json, clean_string, timer, setup_logger


class TestUtils(unittest.TestCase):

    def test_normalize_json_valid(self):
        input_json = '{"b": 2, "a": 1}'
        expected_output = '{\n    "a": 1,\n    "b": 2\n}'
        result = normalize_json(input_json)
        self.assertEqual(result, expected_output)

    def test_normalize_json_invalid(self):
        input_json = "not a json"
        result = normalize_json(input_json)
        self.assertEqual(result, input_json)  # Should return the original invalid string

    def test_clean_string(self):
        input_str = "Hello, World!  \n\t  \r "
        expected_output = "Hello, World!"
        result = clean_string(input_str)
        self.assertEqual(result, expected_output)

    def test_clean_string_with_non_printable(self):
        input_str = "Hello\x00World"
        expected_output = "HelloWorld"
        result = clean_string(input_str)
        self.assertEqual(result, expected_output)

    def test_timer_decorator(self):
        @timer
        def sample_function():
            return "Success"

        result = sample_function()
        self.assertEqual(result, "Success")  # Ensure the function still works as intended

    def test_setup_logger(self):
        logger_name = "test_logger"
        logger = setup_logger(logger_name, level=logging.DEBUG)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, logger_name)
        self.assertEqual(logger.level, logging.DEBUG)

        with self.assertLogs(logger_name, level="DEBUG") as log:
            logger.debug("This is a debug message")
        self.assertIn("This is a debug message", log.output[0])


if __name__ == "__main__":
    unittest.main()
