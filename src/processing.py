"""Process to return the output JSON valid."""
from .function_name import get_function_name
from .utils import read_file, print_token_by_token
from typing import Any
from llm_sdk import Small_LLM_Model  # type: ignore
from .parameters import get_parameters
from .output import generate_json_file
import json


def process(
            model: Small_LLM_Model,
            config: dict[str, Any]
        ) -> None:
    """Get the json output and save it into a file.

    Args:
        model (Small_LLM_Model): Instance of the model llm_sdk
        config (dict[str]): the input get from terminal
    """
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

        prompt_str = prompt["prompt"]

        parameters = get_parameters(
            model, list_functions,
            prompt_str, function_name
        )

        res["prompt"] = prompt_str
        res["name"] = function_name
        res["parameters"] = parameters

        print_token_by_token(json.dumps(res, indent=4))

        result.append(res)

        generate_json_file(config["output"], result)

        i += 1
