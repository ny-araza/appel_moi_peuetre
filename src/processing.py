from .function_name import get_function_name
from .utils import read_file, print_token_by_token
from typing import Any
from llm_sdk import Small_LLM_Model
from .parameters import get_parameters
import json

def process(
            model: Small_LLM_Model, 
            config: dict[str, Any]
        ) -> None:

    prompt_list = read_file(config["input"])
    list_functions = read_file(config["functions_definition"])

    for prompt in prompt_list:
        if not prompt["prompt"].strip(" \t\n\a\b\v\f\r"):
            raise Exception("Prompt not valid")

    result: list[dict[str, Any]] = []

    i = 1

    for prompt in prompt_list:

        print(f"{i} / {len(prompt_list)}")

        res: dict[str, Any] = {}
        function_name = get_function_name(
            model, config, prompt["prompt"]        
        )

        parameters = get_parameters(
            model, list_functions, 
            prompt, function_name
        )

        res["prompt"] = prompt["prompt"]
        res["name"] = function_name
        res["parameters"] = parameters

        print_token_by_token(json.dumps(res, indent=4))

        result.append(res)

        i += 1
