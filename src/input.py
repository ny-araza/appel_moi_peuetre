from pydantic import BaseModel, TypeAdapter
from typing import Any
import json

class FunctionCalling(BaseModel):
    name: str
    description: str
    parameters: dict[Any, Any]
    returns: dict[Any, Any]


class Prompt(BaseModel):
    prompt: str


def load_json(file_path: str) -> list[dict[Any, Any]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def check_prompt_json(file_path: str) -> bool:
    try:
        prompt = load_json(file_path)
        adapter_prompt = TypeAdapter(list[Prompt])
        adapter_prompt.validate_json(json.dumps(prompt))
        return True
    except Exception:
        print("The input json is not a valid JSON")
        return False


def check_function_json(file_path: str) -> bool:
    try:
        function_temp = load_json(file_path)
        adapter_function = TypeAdapter(list[FunctionCalling])
        adapter_function.validate_json(json.dumps(function_temp))
        return True
    except Exception:
        print("The functions definition is not a valid JSON")
        return False


def check_input(config: dict[str, Any]) -> bool:
    if check_prompt_json(config["input"]) and check_function_json(config["functions_definition"]):
        return True
    return False
