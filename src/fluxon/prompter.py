def format_prompt(base_prompt: str, schema: dict, start_tag: str = "BEGIN_JSON", end_tag: str = "END_JSON") -> str:
    """
    Formats a prompt by appending a JSON schema-like description with start and end tags.

    Args:
        base_prompt (str): The initial instruction for the LLM.
        schema (dict): A dictionary representing the JSON schema.
        start_tag (str): The start tag for JSON output.
        end_tag (str): The end tag for JSON output.

    Returns:
        str: A formatted prompt with the schema and tags.
    """
    import json
    schema_str = json.dumps(schema, indent=2)
    return (
        f"{base_prompt}\n\n"
        f"Output the JSON object between the tags:\n"
        f"{start_tag}\n"
        f"{schema_str}\n"
        f"{end_tag}"
    )
