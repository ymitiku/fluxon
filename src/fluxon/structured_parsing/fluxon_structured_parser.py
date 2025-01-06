from fluxon.structured_parsing.commented_json_tokenizer import CommentedJsonTokenizer
from fluxon.structured_parsing.content_tokenizer import ContentTokenizer

class FluxonStructuredParser:
    def __init__(self):
        self.content_tokenizer = ContentTokenizer()
        self.commented_json_tokenizer = CommentedJsonTokenizer()

    def parse(self, input_text: str):
        """
        Parses the given input text, tokenizing both outer free text and inner JSON objects.

        Args:
            input_text (str): The text containing free text and embedded JSON objects.

        Returns:
            list: A list of parsed segments, including free text and detailed JSON objects.
        """
        parsed_output = []
        outer_tokens = self.content_tokenizer.tokenize(input_text)

        for token in outer_tokens:
            if token["type"] == "free_text":
                parsed_output.append({"type": "free_text", "value": token["value"]})
            elif token["type"] == "json_object":
                # Pass the JSON object value to InnerTokenizer for detailed parsing
                inner_tokens = self.commented_json_tokenizer.tokenize(token["value"])
                parsed_output.append({"type": "json_object", "value": inner_tokens})

        return parsed_output
    
    def render(self, parsed_output, compact=False):
        """
        Renders the parsed output into a string.

        Args:
            parsed_output (list): The parsed output from the parse method.
            compact (bool): Whether to render the JSON objects in compact mode. If True comments will be removed.

        Returns:
            str: The rendered string.
        """
        output = ""
        for segment in parsed_output:
            if segment["type"] == "free_text" and not compact:
                output += segment["value"] + "\n"
            elif segment["type"] == "json_object":
                current_output = self.commented_json_tokenizer.render(segment["value"], compact = compact)
                output += current_output + "\n"
        return output
    




if __name__ == "__main__":
    input_text = """
    This is some free text before the JSON.
    {
        "key1": "value1", // Inline comment for key1
        /* Block comment for key2 */
        "key2": { 
            "nestedKey1": "nestedValue1",
          
            "nestedKey2": ["arrayValue1" 123, {"deepKey": "deepValue"}] // Inline comment for nestedKey2
        },
        "key3": "value3"
    }
    More free text after the JSON.
    """

    parser = FluxonStructuredParser()
    result = parser.parse(input_text)
    

    print(parser.render(result, compact=False))
    # print(result)
