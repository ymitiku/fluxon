import unittest
from fluxon.structured_parsing.content_tokenizer import ContentTokenizer, CommentedJsonPartTypes
from fluxon.structured_parsing.exceptions import MalformedJsonError


class TestContentTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = ContentTokenizer()

    def test_free_text(self):
        input_text = "This is some free text."
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["type"], CommentedJsonPartTypes.FREE_TEXT)
        self.assertEqual(tokens[0]["value"], "This is some free text.")

    def test_json_object(self):
        input_text = '{"key1": "value1"}'
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["type"], CommentedJsonPartTypes.JSON_OBJECT)

    def test_mixed_content(self):
        input_text = "Text before JSON. {\"key1\": \"value1\"} Text after JSON."
        tokens = self.tokenizer.tokenize(input_text)
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0]["type"], CommentedJsonPartTypes.FREE_TEXT)
        self.assertEqual(tokens[1]["type"], CommentedJsonPartTypes.JSON_OBJECT)
        self.assertEqual(tokens[2]["type"], CommentedJsonPartTypes.FREE_TEXT)

    def test_malformed_json(self):
        input_text = "{This is not valid JSON"
        with self.assertRaises(MalformedJsonError):
            self.tokenizer.tokenize(input_text)
