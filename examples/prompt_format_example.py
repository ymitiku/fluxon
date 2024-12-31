
import os, sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fluxon.prompter import format_prompt

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
    },
    "required": ["name", "age"]
}

# Step 1: Format the prompt
prompt = format_prompt("Provide user details in JSON format.", schema)
print("Prompt to LLM:\n", prompt)