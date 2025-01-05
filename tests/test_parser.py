import unittest
from fluxon.parser import (
    parse_json_with_recovery,
    trim_to_json,
    add_missing_commas_in_key_value_pairs,
    add_missing_commas_in_arrays,
    fix_common_json_errors,
    extract_json_from_text,
    remove_comments,
    clean_raw_json
)
from fluxon.utils import normalize_json


class TestParser(unittest.TestCase):

    def test_parse_json_with_recovery(self):
        input_json = '{"name": "Alice", "age": 25 "city": "New York"}'
        expected_output = {"name": "Alice", "age": 25, "city": "New York"}
        result = parse_json_with_recovery(input_json)
        self.assertEqual(result, expected_output)

        malformed_json = '{"name": "Alice", "age": "25",}'
        expected_output = {"name": "Alice", "age": "25"}
        result = parse_json_with_recovery(malformed_json)
        self.assertEqual(result, expected_output)

    def test_trim_to_json(self):
        input_text = "Some random text before {\"key\": \"value\"} and some after"
        expected_output = '{"key": "value"}'
        result = trim_to_json(input_text)
        self.assertEqual(result, expected_output)

    def test_add_missing_commas_in_key_value_pairs(self):
        input_json = '{"name": "Alice", "age": 25 "city": "New York"}'
        expected_output = '{"name": "Alice", "age": 25, "city": "New York"}'
        result = add_missing_commas_in_key_value_pairs(input_json)
        self.assertEqual(result, expected_output)

    def test_add_missing_commas_in_arrays(self):
        input_json = '{"array": ["item1" "item2", {"nested": true} 123]}'
        expected_output = '{"array": ["item1", "item2", {"nested": true}, 123]}'
        result = add_missing_commas_in_arrays(input_json)
        self.assertEqual(result, expected_output)

    def test_fix_common_json_errors(self):
        input_json = '{"name": "Alice", "age": 25 "city": "New York"}'
        expected_output = '{"name": "Alice", "age": 25, "city": "New York"}'
        result = fix_common_json_errors(input_json)
        self.assertEqual(result, expected_output)

    def test_extract_json_from_text(self):
        input_text = "BEGIN_JSON{\"key\": \"value\"}END_JSON"
        expected_output = '{"key": "value"}'
        result = extract_json_from_text(input_text)
        self.assertEqual(result, expected_output)

    def test_remove_comments(self):
        input_json = '''
        {
            "name": "Alice", // This is a single-line comment
            "age": 25 /* This is a block comment */
        }
        '''
        expected_output = '''
        {
            "name": "Alice", 
            "age": 25 
        }
        '''
        result = remove_comments(input_json)
        self.assertEqual(result.strip(), expected_output.strip())

    def test_clean_raw_json(self):
        input_text = """
        BEGIN_JSON
        {
            "name": "Alice", // This is a comment
            "age": 25
        }
        END_JSON
        """
        expected_output = normalize_json('{"name": "Alice", "age": 25}')
    
        result = clean_raw_json(input_text)
        print("Expected:", expected_output)
        print("Result:", result)
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
