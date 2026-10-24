from llm_sdk import Small_LLM_Model  # type: ignore
from typing import Any
import json

def get_response(
        model: Small_LLM_Model,
        prompt: str,
        function: dict[str, Any]
        ) -> str:
    """Return the llm response to get parameters

        Args:
            model (Small_LLM_Model): The llm model
            prompt (str): the prompt

        Returns:
            str: The llm response
    """
    input_ids = model.encode(prompt).tolist()[0]
    i = 0
    temp_res = ""
    while i < 200:
        logits = model.get_logits_from_input_ids(input_ids)
        max_token = max(logits)
        token = logits.index(max_token)
        temp = model.decode([token])
        temp_res += temp
        temp_res = parse_res(temp_res, function)
        if "," in temp:
            break
        input_ids.append(token)
        i += 1
    return temp_res

def parse_res(res: str, function: dict[str, Any]) -> str:
    t = res.split(",")
    keys = list(function["parameters"].keys())
    temp_res = ""
    if len(t) >=1:
        for item in t:
            p = item.split(":")
            if len(p) == 2:
                print(keys)
                print(p[0].strip("' "))
                if p[0].strip("' ") in keys:
                    temp_res += f"{p[0].strip("' ")}: {p[1].strip("\" ")}, "
    print(temp_res)
    return temp_res

def convert_str(obj) -> dict:
    if isinstance(obj, dict):
        return {k: str(v) for k, v in obj.items()}
    return obj


def parse_parameters(
        parameters: str,
        function: dict[Any, Any]
        ) -> dict[Any, Any]:
    """Trim the LLM response

        Args:
            parameters (str): the LLM response that will be trim
            function (dict[Any, Any]): The function

        Returns:
            dict[Any, Any]: The parameters dict
    """
    try:
        temp_params = json.loads(
            parameters.strip(" Answer"),
            object_hook=convert_str
        )
    except Exception:
        temp_params = {}
    return cast_parameters(temp_params, function)


def cast_parameters(
        parameters: dict[Any, Any],
        function: dict[Any, Any]
        ) -> dict[Any, Any]:
    """Cast the value of parameters

        Args:
            parameters (str): the LLM response that will be trim
            function (dict[Any, Any]): The function

        Returns:
            dict[Any, Any]: The parameters dict with all value casted
    """
    type_parameters: dict[str, Any] | None = function.get("parameters")
    for key, value in list(parameters.items()):
        if type_parameters:
            if not type_parameters.get(key):
                del parameters[key]
                continue
            if not type_parameters.get(key)["type"]:  # type: ignore
                parameters.update({key: None})
            if type_parameters.get(key)["type"] == "number":  # type: ignore
                if value:
                    try:
                        parameters.update({key: float(value)})
                    except ValueError:
                        parameters.update({key: 0.0})
                else:
                    parameters.update({key: 0.0})
            if type_parameters.get(key)["type"] == "integer":  # type: ignore
                if value:
                    parameters.update({key: int(value)})
            if type_parameters[key]["type"] == "bool" or \
                type_parameters[key]["type"] == "boolean":
                parameters.update({key: value.strip().lower() == "true"})
        else:
            parameters.update({key: None})
    return parameters


def get_parameters(
        model: Small_LLM_Model,
        list_functions: list[dict[Any, Any]],
        prompt: str,
        function_name: str
        ) -> dict[str, Any]:
    """Get all the parameters from each prompt

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

    result: dict[str, Any] = {}

    temp_prompt = [
        "Extract only the parameters defined in FUNCTION PARAMETERS from the USER REQUEST."
        "Do not invent or infer missing values; use null when a required value is absent."
        "Ignore irrelevant information and preserve the user's values exactly whenever possible."
        "Return only a valid JSON object: {'parameter': 'value'}."
        f"FUNCTION: {function_name} | "
        f"DESCRIPTION: {function.get("description")} | "
        f"PARAMETERS: {function.get("parameters")} | "
        f"USER REQUEST: {prompt}"
        "{ "
    ]
    result = parse_parameters(
        get_response(model, temp_prompt[0], function),
        function
        )
    return result
