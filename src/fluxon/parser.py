import json
import re
from json import JSONDecodeError
from fluxon.utils import normalize_json

def parse_json_with_recovery(json_str: str) -> dict:
    """
    Parses and recovers a JSON string, attempting to fix common errors.

    Args:
        json_str (str): The raw JSON string to parse.

    Returns:
        dict: The parsed JSON object, or an empty dictionary if parsing fails.
    """
    try:
        # First attempt: Try parsing the JSON directly
        return json.loads(json_str)
    except JSONDecodeError as e:
        print(f"Initial parsing failed: {e}")
        # Step 1: Remove any extraneous content (non-JSON)
        json_str = clean_raw_json(json_str)
        # Step 2: Fix common errors
        json_str = fix_common_json_errors(json_str)

        # Final attempt to parse
        try:
            output = json.loads(json_str)
            return output
        except JSONDecodeError as final_error:
            print(f"Final parsing failed: {final_error}")
            return {}

def trim_to_json(input_text: str) -> str:
    """
    Trims input to the first JSON-like structure.
    
    Args:
        input_text (str): The raw input text.
    
    Returns:
        str: Trimmed JSON content or the original text if no JSON structure is found.
    """
    try:
        start = input_text.index("{")
        end = input_text.rindex("}")
        return input_text[start:end + 1]
    except ValueError:
        return input_text

def add_missing_commas_in_key_value_pairs(json_str: str) -> str:
    """
    Adds missing commas between key-value pairs in JSON strings, handling both compact and formatted JSON.

    Args:
        json_str (str): The JSON string with potential missing commas.

    Returns:
        str: A JSON string with corrected commas.
    """
    # Regular expression to find key-value pairs
    key_value_regex = r'(?P<key>"[a-zA-Z_][a-zA-Z0-9_]*"|[a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?P<value>"[^"]*"|[0-9]+|true|false|null)'
    
    # Function to decide whether to add a comma
    def replace_missing_commas(match):
        key = match.group('key')
        value = match.group('value')

        # Check the text after the match to decide whether to add a comma
        end_pos = match.end()
        remaining = json_str[end_pos:].lstrip()

        # Add a comma only if there's no existing comma and it's not the last element
        if remaining and not remaining.startswith(('}', ']', ',')):
            return f'{key}: {value},'
        return f'{key}: {value}'

    # Apply the regex substitution
    json_str = re.sub(key_value_regex, replace_missing_commas, json_str)

    # Remove trailing commas from objects and arrays
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)

    return json_str



def add_missing_commas_in_arrays(json_str: str) -> str:
    """
    Fixes missing commas in arrays within a JSON string.

    Args:
        json_str (str): The JSON string with potential missing commas in arrays.

    Returns:
        str: A JSON string with corrected commas in arrays.
    """
    # Regular expression to match valid array elements
    array_element_regex = r'(?<=[}\]0-9"])\s+(?=[{\[]"|null|true|false|[0-9"])'
    
    # Replace missing commas between array elements
    fixed_json = re.sub(array_element_regex, ', ', json_str)
    
    return fixed_json



def fix_common_json_errors(json_str: str) -> str:
    """
    Fixes common JSON errors such as missing commas, trailing commas, and missing quotes around keys.
    
    Args:
        json_str (str): The JSON string with errors.
    
    Returns:
        str: A potentially fixed JSON string.
    """
    # Fix trailing commas in objects and arrays
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)

    # Fix missing commas between object key-value pairs
    json_str = add_missing_commas_in_key_value_pairs(json_str)
    

    # Fix missing commas in arrays
    json_str = add_missing_commas_in_arrays(json_str)
    # Fix missing quotes around keys
    json_str = re.sub(
        r'(\{|,)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:',  # Matches unquoted keys
        r'\1 "\2":', 
        json_str
    )

    return json_str




def extract_json_from_text(input_text: str, start_tag: str = "BEGIN_JSON", end_tag: str = "END_JSON") -> str:
    """
    Extracts JSON content delimited by start and end tags.

    Args:
        input_text (str): The LLM-generated text containing JSON.
        start_tag (str): The start tag indicating the beginning of JSON.
        end_tag (str): The end tag indicating the end of JSON.

    Returns:
        str: Extracted JSON string or an empty string if no valid JSON is found.
    """
    match = re.search(fr"{start_tag}(.*?){end_tag}", input_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def remove_comments(json_text: str) -> str:
    """
    Removes single-line and block comments from JSON-like text.

    Args:
        json_text (str): The JSON string with potential comments.

    Returns:
        str: The cleaned JSON string without comments.
    """
    # Remove single-line comments
    json_text = re.sub(r'//.*', '', json_text)
    # Remove block comments
    json_text = re.sub(r'/\*.*?\*/', '', json_text, flags=re.DOTALL)
    return json_text

def clean_raw_json(input_text: str) -> str:
    """
    Cleans LLM output by extracting JSON content and removing comments.

    Args:
        input_text (str): The raw LLM-generated output.

    Returns:
        str: Cleaned JSON string or an empty string if cleaning fails.
    """
    json_content = extract_json_from_text(input_text)
    if json_content:
        json_content = remove_comments(json_content)
    json_content = trim_to_json(json_content)
    return normalize_json(json_content)
