

class CommentedJsonTokenizer:
    """ Tokenizes and renders JSON-like content. """
    def __init__(self):
        self.tokens = []

    def tokenize(self, input_text: str) -> list:
        """
        Tokenizes the input JSON-like content using a stack-based approach.

        Args:
            input_text (str): The input JSON content.

        Returns:
            list: A list of tokens with their types.
        """
        self.tokens = []
        input_text = input_text.strip()
        if input_text.startswith("{"):
            input_text = input_text[1:]
        if input_text.endswith("}"):
            input_text = input_text[:-1]
        i = 0
        n = len(input_text)

        while i < n:
            char = input_text[i]

            # Start of a key-value pair
            if char == '"':
                key, i = self.extract_key(input_text, i)
                value, comment, value_type, i = self.extract_value_and_comment(input_text, i)
                self.tokens.append({
                    "type": "key_value",
                    "key": key,
                    "value": value,
                    "comment": comment,
                    "value_type": value_type  # Indicates the type of the value
                })

            # Inline comment
            elif input_text[i:i+2] == "//":
                comment, i = self.extract_inline_comment(input_text, i)
                self.tokens.append({
                    "type": "inline_comment",
                    "value": comment,
                    "value_type": "comment"
                })

            # Block comment
            elif input_text[i:i+2] == "/*":
                comment, i = self.extract_block_comment(input_text, i)
                self.tokens.append({
                    "type": "block_comment",
                    "value": comment,
                    "value_type": "comment"
                })

            # Skip whitespace and commas
            elif char in " \t\n,":
                i += 1

            # Unexpected character
            else:

                raise ValueError(f"Unexpected character at position {i}: {char}")

        return self.tokens

    def extract_key(self, input_text: str, start: int) -> tuple:
        """
        Extracts a key from the JSON input.

        Args:
            input_text (str): The input JSON content.
            start (int): The starting position of the key.

        Returns:
            tuple: (key, new_position)
        """
        end = input_text.find('"', start + 1)
        if end == -1:
            raise ValueError("Unterminated key string")
        key = input_text[start + 1:end]
        colon_pos = input_text.find(':', end)
        if colon_pos == -1:
            raise ValueError("Missing colon after key")
        return key, colon_pos + 1

    def look_ahead_remove_whitespace(self, input_text: str, start: int) -> int:
        """
        Looks ahead in the input text to find the next non-whitespace character.

        Args:
            input_text (str): The input JSON content.
            start (int): The starting position to look ahead.

        Returns:
            int: The position of the next non-whitespace character.
        """
        i = start
        while i < len(input_text) and input_text[i] in " \t\n":
            i += 1
        return i

    def extract_value_and_comment(self, input_text: str, start: int) -> tuple:
        """
        Extracts a value and its associated comment (if any).

        Args:
            input_text (str): The input JSON content.
            start (int): The starting position of the value.

        Returns:
            tuple: (value, comment, value_type, new_position)
        """
        i = start
        comment = None

        # Skip whitespace
        i = self.look_ahead_remove_whitespace(input_text, i)

        char = input_text[i]

        # Nested object
        if char == '{':
            nested_object, i = self.extract_nested_structure(input_text, i, '{', '}')
            nested_tokenizer = CommentedJsonTokenizer()
            value = nested_tokenizer.tokenize(nested_object[1:-1])  # Strip outer braces
            value_type = "object"

        # Array
        elif char == '[':
            array_content, i = self.extract_nested_structure(input_text, i, '[', ']')
            value = self.parse_array(array_content[1:-1])  # Strip outer brackets
            value_type = "array"

        # String
        elif char == '"':
            end = input_text.find('"', i + 1)
            if end == -1:
                raise ValueError("Unterminated string value")
            value = input_text[i + 1:end]
            i = end + 1
            value_type = "string"

        # Primitive value
        else:
            end = i
            while end < len(input_text) and input_text[end] not in ",}] \t\n":
                end += 1
            value = eval(input_text[i:end].strip())  # Evaluate primitive value (e.g., number, true, false, null)
            i = end
            value_type = "primitive"

        # Look ahead to handle commas or comments
        i = self.look_ahead_remove_whitespace(input_text, i)
        if i < len(input_text) and input_text[i] == ",":
            i += 1
        i = self.look_ahead_remove_whitespace(input_text, i)

        # Check for inline or block comments
        if input_text[i:i+2] == "//":
            comment, i = self.extract_inline_comment(input_text, i)
        

        return value, comment, value_type, i

    def extract_nested_structure(self, input_text: str, start: int, open_char: str, close_char: str) -> tuple:
        """
        Extracts a nested structure (object or array) using a stack.

        Args:
            input_text (str): The input JSON content.
            start (int): The starting position of the structure.
            open_char (str): The opening character of the structure.
            close_char (str): The closing character of the structure.

        Returns:
            tuple: (nested_content, new_position)
        """
        stack = [open_char]
        i = start + 1
        while stack and i < len(input_text):
            if input_text[i] == open_char:
                stack.append(open_char)
            elif input_text[i] == close_char:
                stack.pop()
            i += 1

        if stack:
            print("stack", stack)
            print("i", i)
            print("input_text", input_text)
            raise ValueError("Unmatched braces or brackets in nested structure")
        return input_text[start:i], i

    def extract_inline_comment(self, input_text: str, start: int) -> tuple:
        """
        Extracts an inline comment.

        Args:
            input_text (str): The input JSON content.
            start (int): The starting position of the comment.

        Returns:
            tuple: (comment, new_position)
        """
        end = input_text.find('\n', start)
        if end == -1:
            end = len(input_text)
        comment = input_text[start + 2:end].strip()
        return comment, end

    def extract_block_comment(self, input_text: str, start: int) -> tuple:
        """
        Extracts a block comment.

        Args:
            input_text (str): The input JSON content.
            start (int): The starting position of the comment.

        Returns:
            tuple: (comment, new_position)
        """
        end = input_text.find('*/', start)
        if end == -1:
            raise ValueError("Unterminated block comment")
        comment = input_text[start + 2:end].strip()
        return comment, end + 2

    def parse_array(self, array_content: str) -> list:
        """
        Parses an array value.

        Args:
            array_content (str): The content of the array.

        Returns:
            list: A list of parsed array elements.
        """
        elements = []
        tokenizer = CommentedJsonTokenizer()
        i = 0
        n = len(array_content)

        while i < n:
            char = array_content[i]
            if char == '{':
                nested_object, i = self.extract_nested_structure(array_content, i, '{', '}')
                elements.append({
                    "type": "nested_object",
                    "value": tokenizer.tokenize(nested_object[1:-1]),
                    "value_type": "object"
                })
            elif char == '"':
                end = array_content.find('"', i + 1)
                if end == -1:
                    raise ValueError("Unterminated string in array")
                elements.append({"type": "string", "value": array_content[i + 1:end], "value_type": "string"})
                i = end + 1
            elif char not in ", \t\n":
                start = i
                while i < n and array_content[i] not in ", \t\n]":
                    i += 1
            
                value = array_content[start:i].strip()
                if value == "true" or value == "false":
                    elements.append({"type": "primitive", "value": value == "true", "value_type": "primitive"})
                else:
                    elements.append({"type": "primitive", "value": eval(value), "value_type": "primitive"})
            else:
                i += 1

        return elements
    

    def render(self, tokens=None, indent=2, level=0, compact=False) -> str:
        """
        Renders the tokenized JSON content into a formatted string.

        Args:
            tokens (list): The tokenized JSON content.
            indent (int): Number of spaces for indentation.
            level (int): Current indentation level (for nested structures).
            comment_style (str): "inline" or "above".
            compact (bool): If True, produces a compact output.

        Returns:
            str: The rendered JSON content.
        """
        if tokens is None:
            tokens = self.tokens

        output = "{\n"
        for token in tokens:
            if token["type"] == "key_value":
                output += self.render_key_value(token, indent, level + 1,  compact)
            elif not compact:
                if token["type"] == "inline_comment":
                    output += self.render_comment(token, indent, level + 1)
                elif token["type"] == "block_comment":
                    output += self.render_comment(token, indent, level + 1)

        output = output.rstrip(",\n") + "\n"

        output += " " * (indent * level) + "}"

        return output

    def render_key_value(self, token, indent, level, compact):
        """
        Renders a key-value pair.

        Args:
            token (dict): The token representing the key-value pair.
            indent (int): Number of spaces for indentation.
            level (int): Current indentation level.
            comment_style (str): "inline" or "above".
            comment (str): The associated comment.
            compact (bool): If True, produces a compact output.

        Returns:
            str: The rendered key-value pair.
        """
        key = token["key"]
        value = token["value"]
        value_type = token["value_type"]
        indent_str = " " * (indent * level)
        key_value_str = f'"{key}": {self.render_value(value, value_type, indent, level, compact)}'
        comment = token["comment"]
        if comment and not compact:
            key_value_str += "  //" + comment.replace("\n", " ")
            
        return f"{indent_str}{key_value_str},\n"
    
    def render_value(self, value, value_type, indent, level, compact):
        """
        Renders a value based on its type.

        Args:
            value (str): The value to render.
            value_type (str): The type of the value.
            indent (int): Number of spaces for indentation.
            level (int): Current indentation level.
            comment_style (str): "inline" or "above".
            comment (str): The associated comment.
            compact (bool): If True, produces a compact output.

        Returns:
            str: The rendered value.
        """
        if value_type == "object":
            return self.render(value, indent, level, compact)
        elif value_type == "array":
            return self.render_array(value, indent, level, compact)
        elif value_type == "string":
            return f'"{value}"'
        else:
            return str(value)
        

    def render_array(self, elements, indent, level, compact):
        """
        Renders an array value.

        Args:
            elements (list): The elements of the array.
            indent (int): Number of spaces for indentation.
            level (int): Current indentation level.
            comment_style (str): "inline" or "above".
            compact (bool): If True, produces a compact output.

        Returns:
            str: The rendered array value.
        """
        indent_str = " " * (indent * level)
        output = "[" 
        for element in elements:
            if element["type"] == "nested_object":
                output += self.render(element["value"], indent, level + 1, compact)
            elif element["type"] == "string":
                output +=   f'"{element["value"]}"'
            else:
                output +=  str(element["value"])
            output += ", "
        output = output.rstrip(", ") + "\n" + indent_str + "]"
        return output
    
    def render_comment(self, token, indent, level):
        """
        Renders a comment.

        Args:
            token (dict): The token representing the comment.
            indent (int): Number of spaces for indentation.
            level (int): Current indentation level.
            comment_style (str): "inline" or "above".
            comment (str): The associated comment.
            compact (bool): If True, produces a compact output.

        Returns:
            str: The rendered comment.
        """
        indent_str = " " * (indent * level)
        comment = token["value"]
        if token["type"] == "inline_comment":
            return f"{indent_str}// {comment}\n"
        else:
            return f"{indent_str}/* {comment} */\n"
        
    

