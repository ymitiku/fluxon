from jsonschema import validate, ValidationError
from pydantic import BaseModel

def validate_with_schema(json_obj: dict, schema: dict) -> bool:
    """
    Validates a JSON object against a schema.

    Args:
        json_obj (dict): The JSON object to validate.
        schema (dict): The JSON Schema dictionary.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        validate(instance=json_obj, schema=schema)
        return True
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False


def generate_schema(model: BaseModel) -> dict:
    """
    Generates a JSON schema from a Pydantic model.

    Args:
        model (BaseModel): The Pydantic model class.

    Returns:
        dict: The generated JSON schema.
    """
    return model.schema()


def repair_with_schema(json_obj: dict, schema: dict) -> dict:
    """
    Repairs a JSON object by filling missing fields with default values from a schema.

    Args:
        json_obj (dict): The JSON object to repair.
        schema (dict): The JSON Schema dictionary.

    Returns:
        dict: The repaired JSON object.
    """
    for key, value in schema.get("properties", {}).items():
        if key not in json_obj and "default" in value:
            json_obj[key] = value["default"]
    return json_obj
