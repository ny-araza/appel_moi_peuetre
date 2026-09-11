from pydantic import BaseModel, TypeAdapter, Field
from typing import Any
import json


class FunctionCalling(BaseModel):
    """Represents the input model (function calling).

        This class allows you to validate that the 
        function calling.json is a valid JSON file.

        Attributes:
            name (str): the function name
            description (str): description of what the function does
            parameters (dict[str, Any]): List of the parameters of the function
            returns (dict[str, Any]): The return type of the function

    """
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    parameters: dict[Any, Any]
    returns: dict[Any, Any]


class Prompt(BaseModel):
    """Represents the input model (prompt)

        This class allows you to validate that the 
        prompt.json is a valid JSON file.

        Attributes:
            prompt (str): The prompt 
    """
    prompt: str = Field(..., min_length=1)


def load_json(file_path: str) -> list[dict[Any, Any]]:
    """Load the json in the JSON file to assign it into a variable

        Args:
            file_path (str): the filepath of the JSON

        Returns:
            list[dict[Any, Any]]: The json load from the file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data: list[dict[Any, Any]] = json.load(f)
    return data


def check_prompt_json(file_path: str) -> bool:
    """Check if the prompt JSON is a valid JSON
    
        Args:
            file_path (str): the filepath of the JSON

        Returns:
            bool: Return True if its a valid JSON a False if its not
    """
    try:
        prompt = load_json(file_path)
        adapter_prompt = TypeAdapter(list[Prompt])
        adapter_prompt.validate_json(json.dumps(prompt))
        return True
    except Exception:
        print("The input json is not a valid JSON")
        return False


def check_function_json(file_path: str) -> bool:
    """Check if the function_calling JSON is a valid JSON
    
        Args:
            file_path (str): the filepath of the JSON

        Returns:
            bool: Return True if its a valid JSON a False if its not
    """
    try:
        function_temp = load_json(file_path)
        adapter_function = TypeAdapter(list[FunctionCalling])
        adapter_function.validate_json(json.dumps(function_temp))
        return True
    except Exception:
        print("The functions definition is not a valid JSON")
        return False


def check_input(config: dict[str, Any]) -> bool:
    """Check the both input
        
        Args:
            config (dict[str, Any]): All parameters

        Returns:
            bool: Return True if its a valid JSON a False if its not
    """
    if check_prompt_json(config["input"]) and \
            check_function_json(config["functions_definition"]):
        return True
    return False
