import unittest
from fluxon.structured_parsing.content_tokenizer import ContentTokenizer


class TestContentTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = ContentTokenizer()

    def test_free_text(self):
        input_text = "This is some free text."
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["type"], "free_text")
        self.assertEqual(tokens[0]["value"], "This is some free text.")

    def test_json_object(self):
        input_text = '{"key1": "value1"}'
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["type"], "json_object")

    def test_mixed_content(self):
        input_text = "Text before JSON. {\"key1\": \"value1\"} Text after JSON."
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0]["type"], "free_text")
        self.assertEqual(tokens[1]["type"], "json_object")
        self.assertEqual(tokens[2]["type"], "free_text")

    def test_malformed_json(self):
        input_text = "{This is not valid JSON"
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize(input_text)
