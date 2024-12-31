import json
import logging
import time

def normalize_json(json_str: str) -> str:
    """
    Normalizes a JSON string to have consistent formatting.

    Args:
        json_str (str): The JSON string to normalize.

    Returns:
        str: A normalized JSON string.
    """
    try:
        json_obj = json.loads(json_str)
        return json.dumps(json_obj, indent=4, sort_keys=True)
    except json.JSONDecodeError:
        return json_str  # Return the original if parsing fails



def clean_string(input_str: str) -> str:
    """
    Removes extraneous whitespace and non-printable characters.

    Args:
        input_str (str): The input string to clean.

    Returns:
        str: A cleaned string.
    """
    return ''.join(c for c in input_str if c.isprintable()).strip()





def timer(func):
    """
    Decorator to time a function's execution.

    Args:
        func (callable): The function to time.

    Returns:
        callable: The wrapped function with timing.
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {end - start:.4f} seconds")
        return result
    return wrapper





def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a custom logger.

    Args:
        name (str): The logger's name.
        level (int): The logging level (default: INFO).

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
