"""Get all the parameters of each prompt."""

from llm_sdk import Small_LLM_Model  # type: ignore
from typing import Any
import json


def get_response(
        model: Small_LLM_Model,
        prompt: str,
        function: dict[str, Any],
        keys: list[str]
        ) -> dict[Any, Any]:
    """Return the llm response to get parameters.

    Args:
        model (Small_LLM_Model): The llm model
        prompt (str): the prompt

    Returns:
        str: The llm response
    """
    input_ids = model.encode(prompt).tolist()[0]
    i = 0
    temp_res = ""
    params: dict[Any, Any] = {}
    while i < 200:
        logits = model.get_logits_from_input_ids(input_ids)
        max_token = max(logits)
        token = logits.index(max_token)
        temp = model.decode([token])
        temp_res += temp
        if check_valid_params(temp_res, keys):
            params = json.loads(temp_res)
            break
        input_ids.append(token)
        i += 1
    return params


def check_valid_params(temp_json: str, keys: list[str]) -> bool:
    """Constraint decoding to get the parameters.

    Args:
        temp_json (str): the params reurned by the llm
        keys (list[str]): the list of key from function definition
    Returns:
        bool: the parameters are valid or not
    """
    if "}" in temp_json:
        try:
            params: dict[Any, Any] = json.loads(temp_json)
            if len(list(params.keys())) == len(keys):
                for k in list(params.keys()):
                    if k not in keys or not params[k]:
                        return False
                return True
            return True
        except Exception:
            return False
    return False


def format_value(
        params: dict[Any, Any],
        function_params: dict[Any, Any]
        ) -> dict[Any, Any]:
    """Format the parameters value.

    Args:
        params (dict[Any, Any]): the params return by the llm
        function_params (dict[Any, Any]): the function parameters
    Returns:
        dict[Any, Any]: the params dict zith the right value
    """
    for key, value in params.items():
        try:
            temp = function_params["parameters"][key]
            if temp.get("type", "string") == "number":
                try:
                    params[key] = float(value)
                except ValueError:
                    params[key] = str(value)
            elif temp.get("type", "string") == "integer":
                try:
                    params[key] = int(value)
                except ValueError:
                    params[key] = str(value)
            elif temp.get("type", "string") == "boolean" \
                    or temp.get("type", "string") == "bool":
                res: bool = False
                if value.lower() == "true":
                    res = True
                params[key] = res
            else:
                params[key] = str(value)
        except KeyError:
            params[key] = str(value)
    return params


def get_parameters(
        model: Small_LLM_Model,
        list_functions: list[dict[Any, Any]],
        prompt: str,
        function_name: str
        ) -> dict[str, Any]:
    """Get all the parameters from each prompt.

    Args:
        model (Small_LLM_Model): The LLM model
        res_json (list[dict[Any, Any]]): The output json
        list_functions (list[dict[Any, Any]]): The functions list

    Returns:
        list[dict[Any, Any]]: The output value
    """
    function = {}
    for item in list_functions:
        if item["name"] == function_name:
            function.update(item)

    if not function.get("parameters", ""):
        return {}
    result: dict[str, Any] = {}

    keys_params = list(function["parameters"].keys())

    temp_prompt = [
        "You are a function argument extraction agent. "
        "Extract parameters strictly using the provided context:"
        "Your task is to extract the arguments needed to call the function."
        f"FUNCTION: {function["name"]}\n"
        f"DESCRIPTION : {function["description"]}\n"
        f"PARAMETERS:: {function["parameters"]}\n"
        f"USER REQUEST : {prompt}\n"
        """Rules:
        1. Preserve exact user values.
        2. Extract ONLY parameters defined in the function.
        3. Do NOT invent, guess, or infer values.
        4. Set missing required parameters to null.
        5. Output ONLY a valid JSON object: {"param_name": "value"}.
        No explanations or extra text.
        Output:"""
    ]
    temp_parameters = get_response(
        model, temp_prompt[0],
        function, keys_params
    )

    result = format_value(temp_parameters, function)

    return result
