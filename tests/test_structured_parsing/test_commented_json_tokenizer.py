import unittest
from fluxon.structured_parsing.commented_json_tokenizer import CommentedJsonTokenizer
from fluxon.utils import normalize_json


class TestCommentedJsonTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = CommentedJsonTokenizer()

    def test_simple_key_value(self):
        input_text = '{"key1": "value1"}'
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["key"], "key1")
        self.assertEqual(tokens[0]["value"], "value1")
        self.assertEqual(tokens[0]["value_type"], "string")

    def test_nested_object(self):
        input_text = '{"key1": {"nestedKey": "nestedValue"}}'
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["key"], "key1")
        self.assertEqual(tokens[0]["value_type"], "object")
        self.assertEqual(tokens[0]["value"][0]["key"], "nestedKey")
        self.assertEqual(tokens[0]["value"][0]["value"], "nestedValue")

    def test_array_with_mixed_types(self):
        input_text = '{"key1": ["string", 123, true]}'
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["key"], "key1")
        self.assertEqual(tokens[0]["value_type"], "array")
        self.assertEqual(len(tokens[0]["value"]), 3)

    def test_inline_comment(self):
        input_text = '{"key1": "value1" // Inline comment\n}'
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["comment"], "Inline comment")

    def test_block_comment(self):
        input_text = '{"key1": "value1", /* Block comment */ "key2": "value2"}'
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[1]["value"], "Block comment")

    def test_render_pretty(self):
        input_text = '{"key1": "value1", "key2": {"nestedKey": "nestedValue"}}'
        tokens = self.tokenizer.tokenize(input_text)
        rendered = self.tokenizer.render(tokens, indent=4, compact=False)
        self.assertIn('"key1": "value1"', rendered)
        self.assertIn('"nestedKey": "nestedValue"', rendered)

    def test_render_compact(self):
        input_text = '{"key1": "value1", "key2": {"nestedKey": "nestedValue"}}'
        tokens = self.tokenizer.tokenize(input_text)
        rendered = self.tokenizer.render(tokens, compact=True)
        rendered = normalize_json(rendered)
        expected = normalize_json('{"key1":"value1","key2":{"nestedKey":"nestedValue"}}')


        self.assertEqual(rendered, expected)
