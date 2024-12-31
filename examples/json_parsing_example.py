
import os, sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fluxon.parser import clean_llm_output, parse_json_with_recovery

# Malformed JSON output from LLM
llm_output = """
LLM Thoughts: Here is the JSON data:
BEGIN_JSON
{
    "name": "Alice", "age": 25 /// This is a comment. Missing comma after 25
    "city": "New York",
    "grades": [90, 85  95 
    "Json is fun!", "Comma, inside text"] // Missing comma after 85
}
Hello world
END_JSON
"""

# Step 1: Clean the LLM output
cleaned_output = clean_llm_output(llm_output)

# Step 2: Parse and recover JSON
parsed_output = parse_json_with_recovery(cleaned_output)

print("Parsed JSON:\n", parsed_output)
