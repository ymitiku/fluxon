import re
from enum import Enum
from fluxon.structured_parsing.exceptions import UnRecognizedInputFormatError, MalformedJsonError



class CommentedJsonPartTypes(Enum):
    FREE_TEXT = "free_text"
    JSON_OBJECT = "json_object"

class CommentedJsonPart:
    def __init__(self, part_type: CommentedJsonPartTypes, value: str):
        self.part_type = part_type
        self.value = value


class ContentTokenizer:
    """ Tokenizes mixed content containing free text and JSON objects. """
    TOKEN_PATTERNS = {
        "free_text": r'[^{}]+',  # Matches free text (avoids overlapping with JSON objects)
    }

    def __init__(self):
        self.tokens = []

    def extract_nested_json(self, input_text: str):
        """
        Extracts the first nested JSON object from the input text.

        Args:
            input_text (str): The text containing JSON objects.

        Returns:
            tuple: A tuple (json_object, remaining_text) where json_object is the matched JSON
                   and remaining_text is the text after the JSON object.
        """
        stack = []
        json_start = None

        for i, char in enumerate(input_text):
            if char == '{':
                if not stack:
                    json_start = i  # Mark the start of the JSON object
                stack.append(char)
            elif char == '}':
                stack.pop()
                if not stack:  # Found the matching closing brace
                    return input_text[json_start:i + 1], input_text[i + 1:]

        return None, input_text  # No valid JSON found

    def tokenize(self, input_text: str) -> list:
        """
        Tokenizes the input text into free text and JSON objects.

        Args:
            input_text (str): The input containing mixed content.

        Returns:
            list: A list of tokens with their types.
        """
        self.tokens = []

        while input_text:
            input_text = input_text.strip()

            # Extract JSON object if it starts with '{'
            if input_text.startswith('{'):
                json_object, input_text = self.extract_nested_json(input_text)
                if json_object:
                    self.tokens.append({"type": CommentedJsonPartTypes.JSON_OBJECT, "value": json_object})
                else:
                    raise MalformedJsonError("Malformed JSON detected")

            # Extract free text
            else:
                match = re.match(self.TOKEN_PATTERNS["free_text"], input_text)
                if match:
                    self.tokens.append({"type": CommentedJsonPartTypes.FREE_TEXT, "value": match.group(0).strip()})
                    input_text = input_text[match.end():]
                else:
                    raise UnRecognizedInputFormatError(f"Unrecognized input: {input_text[:30]}")

        return self.tokens
