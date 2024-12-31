import csv
import json
import yaml
import xmltodict
from io import StringIO

def yaml_to_json(yaml_content: str) -> str:
    """
    Converts YAML content to a JSON string.

    Args:
        yaml_content (str): The YAML string to convert.

    Returns:
        str: The equivalent JSON string.
    """
    try:
        yaml_data = yaml.safe_load(yaml_content)
        return json.dumps(yaml_data, indent=4)
    except yaml.YAMLError as e:
        print(f"YAML to JSON conversion error: {e}")
        return ""

def validate_yaml_with_schema(yaml_content: str, schema: dict) -> bool:
    """
    Validates YAML content against a JSON Schema.

    Args:
        yaml_content (str): The YAML string to validate.
        schema (dict): The JSON Schema dictionary.

    Returns:
        bool: True if valid, False otherwise.
    """
    from jsonschema import validate, ValidationError

    try:
        yaml_data = yaml.safe_load(yaml_content)
        validate(instance=yaml_data, schema=schema)
        return True
    except (yaml.YAMLError, ValidationError) as e:
        print(f"Validation error: {e}")
        return False
    

def csv_to_json(csv_content: str) -> str:
    """
    Converts CSV content to a JSON string.

    Args:
        csv_content (str): The CSV string to convert.

    Returns:
        str: The equivalent JSON string.
    """
    try:
        csv_reader = csv.DictReader(StringIO(csv_content))
        json_data = [row for row in csv_reader]
        return json.dumps(json_data, indent=4)
    except csv.Error as e:
        print(f"CSV to JSON conversion error: {e}")
        return ""
    




def xml_to_json(xml_content: str) -> str:
    """
    Converts XML content to a JSON string.

    Args:
        xml_content (str): The XML string to convert.

    Returns:
        str: The equivalent JSON string.
    """
    try:
        xml_data = xmltodict.parse(xml_content)
        return json.dumps(xml_data, indent=4)
    except Exception as e:
        print(f"XML to JSON conversion error: {e}")
        return ""

