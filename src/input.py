from pydantic import BaseModel, TypeAdapter, Field, ValidationError, ConfigDict
from typing import Any
from json import load, dumps, JSONDecodeError


class FunctionCalling(BaseModel):
    """Represents the input model (function calling).

        This class allows you to validate that the
        function calling.json is a valid JSON file.

        Attributes:
            name (str): the function name
            description (str): description of what the function does
            parameters (dict[str, Any]): List of the parameters of the function
            returns (dict[str, Any]): The return type of the function
            model_config (native attribut fron pydantic that doesn't
            allow an extra key for the model)

    """
    model_config = ConfigDict(extra="forbid")
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
            model_config (native attribut fron pydantic that doesn't
            allow an extra key for the model)
    """
    model_config = ConfigDict(extra="forbid")
    prompt: str = Field(..., min_length=1)


def load_json(file_path: str) -> list[dict[Any, Any]]:
    """Load the json in the JSON file to assign it into a variable

        Args:
            file_path (str): the filepath of the JSON

        Returns:
            list[dict[Any, Any]]: The json load from the file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data: list[dict[Any, Any]] = load(f, object_pairs_hook=check_duplicate_key)
    return data


def check_duplicate_key(item: dict) -> bool:
    seen = {}
    for key, value in item:
        if key in seen:
            raise Exception("Key must be unique")
        else:
            seen[key] = value
    return seen


def check_prompt_json(file_path: str) -> bool:
    """Check if the prompt JSON is a valid JSON

        Args:
            file_path (str): the filepath of the JSON

        Returns:
            bool: Return True if its a valid JSON a False if its not
    """
    try:

        try:
            prompt = load_json(file_path)
        except JSONDecodeError as e:
            raise Exception(e)

        if not prompt:
            raise Exception("JSON List must have one key at least")
        adapter_prompt = TypeAdapter(list[Prompt])
        adapter_prompt.validate_json(dumps(prompt))
        return True
    except ValidationError as e:
        for err in e.errors():
            print(err["msg"])
        return False


def check_function_json(file_path: str) -> bool:
    """Check if the function_calling JSON is a valid JSON

        Args:
            file_path (str): the filepath of the JSON

        Returns:
            bool: Return True if its a valid JSON a False if its not
    """
    try:

        try:
            function_temp = load_json(file_path)
        except JSONDecodeError as e:
            raise Exception(e)

        if not function_temp:
            raise ("JSON List must have one key at least")
        adapter_function = TypeAdapter(list[FunctionCalling])
        adapter_function.validate_json(dumps(function_temp))
        return True
    except ValidationError as e:
        for err in e.errors():
            print(err["msg"])
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
