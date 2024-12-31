import unittest
from fluxon.prompter import format_prompt


class TestPrompter(unittest.TestCase):

    def test_format_prompt_basic(self):
        base_prompt = "Generate user details."
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "required": ["name", "age"]
        }
        start_tag = "BEGIN_JSON"
        end_tag = "END_JSON"

        expected_output = (
            "Generate user details.\n\n"
            "Output the JSON object between the tags:\n"
            "BEGIN_JSON\n"
            "{\n"
            "  \"type\": \"object\",\n"
            "  \"properties\": {\n"
            "    \"name\": {\n"
            "      \"type\": \"string\"\n"
            "    },\n"
            "    \"age\": {\n"
            "      \"type\": \"integer\"\n"
            "    }\n"
            "  },\n"
            "  \"required\": [\n"
            "    \"name\",\n"
            "    \"age\"\n"
            "  ]\n"
            "}\n"
            "END_JSON"
        )
        result = format_prompt(base_prompt, schema, start_tag, end_tag)
        self.assertEqual(result, expected_output)

    def test_format_prompt_custom_tags(self):
        base_prompt = "Describe a car."
        schema = {
            "type": "object",
            "properties": {
                "make": {"type": "string"},
                "model": {"type": "string"},
                "year": {"type": "integer"},
            },
            "required": ["make", "model"]
        }
        start_tag = "START_CAR_JSON"
        end_tag = "END_CAR_JSON"

        expected_output = (
            "Describe a car.\n\n"
            "Output the JSON object between the tags:\n"
            "START_CAR_JSON\n"
            "{\n"
            "  \"type\": \"object\",\n"
            "  \"properties\": {\n"
            "    \"make\": {\n"
            "      \"type\": \"string\"\n"
            "    },\n"
            "    \"model\": {\n"
            "      \"type\": \"string\"\n"
            "    },\n"
            "    \"year\": {\n"
            "      \"type\": \"integer\"\n"
            "    }\n"
            "  },\n"
            "  \"required\": [\n"
            "    \"make\",\n"
            "    \"model\"\n"
            "  ]\n"
            "}\n"
            "END_CAR_JSON"
        )
        result = format_prompt(base_prompt, schema, start_tag, end_tag)
        self.assertEqual(result, expected_output)

    def test_format_prompt_empty_schema(self):
        base_prompt = "Generate a JSON object."
        schema = {}
        start_tag = "BEGIN_JSON"
        end_tag = "END_JSON"

        expected_output = (
            "Generate a JSON object.\n\n"
            "Output the JSON object between the tags:\n"
            "BEGIN_JSON\n"
            "{}\n"
            "END_JSON"
        )
        result = format_prompt(base_prompt, schema, start_tag, end_tag)
        self.assertEqual(result, expected_output)

    def test_format_prompt_minimal_schema(self):
        base_prompt = "Generate a minimal schema."
        schema = {"type": "object"}
        start_tag = "BEGIN_JSON"
        end_tag = "END_JSON"

        expected_output = (
            "Generate a minimal schema.\n\n"
            "Output the JSON object between the tags:\n"
            "BEGIN_JSON\n"
            "{\n"
            "  \"type\": \"object\"\n"
            "}\n"
            "END_JSON"
        )
        result = format_prompt(base_prompt, schema, start_tag, end_tag)
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
