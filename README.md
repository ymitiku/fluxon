# Fluxon version 0.0.2"

**Pronunciation**: *Fluhk-sawn*

Fluxon is a Python library designed for crafting structured prompts and parsing structured outputs, with a primary focus on JSON. Fluxon bridges the gap between human-readable prompts and machine-readable structured data, enabling seamless interaction with large language models (LLMs). It ensures robust error recovery, validation, and the generation of well-structured prompts tailored to LLMs.

## Features

- **Prompt Formatting**: Guides LLMs to generate structured outputs using schemas and custom tags.
- **Schema-Driven Parsing**: Validates and parses outputs with tools like YAML, JSON Schema, or Pydantic classes.
- **Error-Tolerant Parsing**: Repairs common JSON issues such as missing commas, invalid formatting, and unquoted keys.
- **Comprehensive Validation**: Ensures outputs conform to expected structures using schema validation.
- **Preprocessing Tools**: Cleans LLM-generated outputs by removing comments and isolating JSON content.
- **Lightweight and Modular Design**: Optimized for Python-based workflows.

## Installation

To install Fluxon, use pip:

```bash
pip install fluxon
```

## Usage

### 1. Prompt Formatting

Create structured prompts to guide LLMs:

```python
from fluxon.prompter import format_prompt

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name", "age"]
}

prompt = "Provide user details in JSON format."
formatted_prompt = format_prompt(prompt, schema)
print("Prompt to LLM:", formatted_prompt)
```

#### Output:

```
Provide user details in JSON format.

Output the JSON object between the tags:
BEGIN_JSON
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "age": {
      "type": "integer"
    }
  },
  "required": [
    "name",
    "age"
  ]
}
END_JSON
```

### 2. Parsing and Error Recovery

Use Fluxon to clean and parse LLM outputs:

```python
from fluxon.parser import clean_llm_output, parse_json_with_recovery

llm_output = """
BEGIN_JSON
{
    "name": "Alice",
    "age": 25
    "city": "New York"
}
END_JSON
"""

# Step 1: Clean the LLM output
cleaned_output = clean_llm_output(llm_output)

# Step 2: Parse and recover JSON
parsed_json = parse_json_with_recovery(cleaned_output)
print("Parsed JSON:", parsed_json)
```

#### Output:

```json
{
    "name": "Alice",
    "age": 25,
    "city": "New York"
}
```

### 3. Validation and Repair

Validate or repair JSON outputs using schemas:

```python
from fluxon.validator import validate_with_schema, repair_with_schema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "default": 30}
    },
    "required": ["name", "age"]
}

json_obj = {"name": "Alice"}

# Validate the JSON object
is_valid = validate_with_schema(json_obj, schema)
print("Is valid:", is_valid)

# Repair the JSON object by filling defaults
repaired_json = repair_with_schema(json_obj, schema)
print("Repaired JSON:", repaired_json)
```

#### Output:

```
Is valid: False
Repaired JSON: {"name": "Alice", "age": 30}
```

## Contributing

Contributions are welcome! Please submit pull requests or report issues on the [GitHub repository](https://github.com/ymitiku/fluxon).

## License

Fluxon is licensed under the [Apache License 2.0](LICENSE).

---

Start building error-resilient, structured workflows with Fluxon today!

