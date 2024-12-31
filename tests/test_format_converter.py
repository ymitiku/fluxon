import unittest
from fluxon.format_converter import yaml_to_json, validate_yaml_with_schema, csv_to_json, xml_to_json


class TestFormatConverter(unittest.TestCase):

    def test_yaml_to_json_valid(self):
        yaml_content = """
        name: Alice
        age: 25
        city: New York
        """
        expected_output = '{\n    "name": "Alice",\n    "age": 25,\n    "city": "New York"\n}'
        result = yaml_to_json(yaml_content)
        self.assertEqual(result, expected_output)

    def test_yaml_to_json_invalid(self):
        yaml_content = """
        name: Alice
        age: 25:
        city: New York
        """
        result = yaml_to_json(yaml_content)
        self.assertEqual(result, "")  # Should return an empty string on error

    def test_validate_yaml_with_schema_valid(self):
        yaml_content = """
        name: Alice
        age: 25
        city: New York
        """
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "city": {"type": "string"}
            },
            "required": ["name", "age", "city"]
        }
        self.assertTrue(validate_yaml_with_schema(yaml_content, schema))

    def test_validate_yaml_with_schema_invalid(self):
        yaml_content = """
        name: Alice
        age: "twenty-five"
        """
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name", "age"]
        }
        self.assertFalse(validate_yaml_with_schema(yaml_content, schema))

    def test_csv_to_json_valid(self):
        csv_content = "name,age,city\nAlice,25,New York\nBob,30,San Francisco"
        expected_output = (
            '[\n'
            '    {\n'
            '        "name": "Alice",\n'
            '        "age": "25",\n'
            '        "city": "New York"\n'
            '    },\n'
            '    {\n'
            '        "name": "Bob",\n'
            '        "age": "30",\n'
            '        "city": "San Francisco"\n'
            '    }\n'
            ']'
        )
        result = csv_to_json(csv_content)
        self.assertEqual(result, expected_output)

    def test_csv_to_json_invalid(self):
        csv_content = "name,age,city\nAlice,25\nBob,San Francisco"
        result = csv_to_json(csv_content)
        expected_output = """[
    {
        "name": "Alice",
        "age": "25",
        "city": null
    },
    {
        "name": "Bob",
        "age": "San Francisco",
        "city": null
    }
]"""
        self.assertEqual(result, expected_output)  # Should return an empty string on error

    def test_xml_to_json_valid(self):
        xml_content = """
        <user>
            <name>Alice</name>
            <age>25</age>
            <city>New York</city>
        </user>
        """
        expected_output = (
            '{\n'
            '    "user": {\n'
            '        "name": "Alice",\n'
            '        "age": "25",\n'
            '        "city": "New York"\n'
            '    }\n'
            '}'
        )
        result = xml_to_json(xml_content)
        self.assertEqual(result, expected_output)

    def test_xml_to_json_invalid(self):
        xml_content = """
        <user>
            <name>Alice</name>
            <age>25<age>
        </user>
        """
        result = xml_to_json(xml_content)
        self.assertEqual(result, "")  # Should return an empty string on error


if __name__ == "__main__":
    unittest.main()
