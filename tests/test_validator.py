import unittest
from jsonschema import ValidationError
from pydantic import BaseModel
from fluxon.validator import validate_with_schema, generate_schema, repair_with_schema


class TestValidator(unittest.TestCase):

    def test_validate_with_schema_valid(self):
        json_obj = {"name": "Alice", "age": 25}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "required": ["name", "age"]
        }
        self.assertTrue(validate_with_schema(json_obj, schema))

    def test_validate_with_schema_invalid(self):
        json_obj = {"name": "Alice"}  # Missing "age"
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "required": ["name", "age"]
        }
        self.assertFalse(validate_with_schema(json_obj, schema))

    def test_generate_schema(self):
        class User(BaseModel):
            name: str
            age: int

        expected_schema = {
            "title": "User",
            "type": "object",
            "properties": {
                "name": {"title": "Name", "type": "string"},
                "age": {"title": "Age", "type": "integer"}
            },
            "required": ["name", "age"]
        }
        self.assertEqual(generate_schema(User), expected_schema)

    def test_repair_with_schema(self):
        json_obj = {"name": "Alice"}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "default": 30}
            },
            "required": ["name", "age"]
        }
        expected_output = {"name": "Alice", "age": 30}
        self.assertEqual(repair_with_schema(json_obj, schema), expected_output)

    def test_repair_with_schema_no_defaults(self):
        json_obj = {"name": "Alice"}
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
        expected_output = {"name": "Alice"}
        self.assertEqual(repair_with_schema(json_obj, schema), expected_output)


if __name__ == "__main__":
    unittest.main()
