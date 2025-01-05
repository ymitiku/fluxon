import unittest
from fluxon.structured_parsing.structured_parser import FluxonStructuredParser
from fluxon.utils import normalize_json


class TestFluxonStructuredParser(unittest.TestCase):
    def setUp(self):
        self.parser = FluxonStructuredParser()

    def test_free_text_only(self):
        input_text = "This is just some free text."
        result = self.parser.parse(input_text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "free_text")
        self.assertEqual(result[0]["value"], "This is just some free text.")

    def test_json_object_only(self):
        input_text = '{"key1": "value1"}'
        result = self.parser.parse(input_text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "json_object")
        self.assertEqual(len(result[0]["value"]), 1)

    def test_mixed_content(self):
        input_text = "Text before JSON. {\"key1\": \"value1\"} Text after JSON."
        result = self.parser.parse(input_text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["type"], "free_text")
        self.assertEqual(result[1]["type"], "json_object")
        self.assertEqual(result[2]["type"], "free_text")

    def test_render_pretty(self):
        input_text = '{"key1": "value1", "key2": {"nestedKey": "nestedValue"}}'
        result = self.parser.parse(input_text)
        rendered = self.parser.render(result, compact=False)
        self.assertIn('"key1": "value1"', rendered)
        self.assertIn('"nestedKey": "nestedValue"', rendered)

    def test_render_compact(self):
        input_text = '{"key1": "value1", "key2": {"nestedKey": "nestedValue"}}'
        result = self.parser.parse(input_text)
        rendered = normalize_json(self.parser.render(result, compact=True))
        self.assertEqual(rendered, normalize_json('{"key1":"value1","key2":{"nestedKey":"nestedValue"}}'))
