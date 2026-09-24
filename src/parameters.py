from llm_sdk import Small_LLM_Model  # type: ignore
from typing import Any
import json


def get_response(
        model: Small_LLM_Model,
        prompt: str,
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
    while i < 60:
        logits = model.get_logits_from_input_ids(input_ids)
        max_token = max(logits)
        token = logits.index(max_token)
        temp = model.decode([token])
        temp_res += temp
        if "}\n" in temp:
            break
        input_ids.append(token)
        i += 1
    return temp_res


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
        temp_params = json.loads(parameters.strip(" Answer"))
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
                    parameters.update({key: float(value)})
            if type_parameters.get(key)["type"] == "integer":
                if value:
                    parameters.update({key: int(value)})
            if type_parameters[key]["type"] == "bool":
                parameters.update({key: value.strip().lower() == "true"})
        else:
            parameters.update({key: None})
    return parameters


def get_parameters(
        model: Small_LLM_Model,
        res_json: list[dict[Any, Any]],
        list_functions: list[dict[Any, Any]],
        prompt_list: list[dict[str, str]]
        ) -> list[dict[Any, Any]]:
    """Get all the parameters from each prompt

        Args:
            model (Small_LLM_Model): The LLM model
            res_json (list[dict[Any, Any]]): The output json
            list_functions (list[dict[Any, Any]]): The functions list

        Returns:
            list[dict[Any, Any]]: The output value
    """
    function = {}
    print("Get the parameters:")
    for index, r in enumerate(res_json, start=1):
        for item in list_functions:
            if item["name"] == r["name"]:
                function.update(item)

        temp_prompt = [
                    f"You are a function calling argument extraction agent."
                    "Your task is to extract the arguments needed "
                    "to call the function..\n"
                    f"FUNCTION: {function.get("name")}\n"
                    f"{function.get("descriptions")}"
                    f"Function parameters: {function.get("parameters")}\n "
                    f"User request: {r.get("prompt")}"
                    "Rules:\n"
                    "Extract ONLY parameters that are "
                    "defined in the function parameters.\n"
                    "Match information from the user request "
                    "to the corresponding parameter."
                    "Do NOT invent, guess, or infer values "
                    "that are not explicitly provided."
                    "If a required parameter is not "
                    "provided, set its value to null."
                    "Ignore information that is not "
                    "relevant to the function."
                    "Preserve the value exactly as given by "
                    "the user whenever possible."
                    "Return ONLY a JSON object containing the "
                    "parameter names and their values."
                    "Do not add explanations, comments, "
                    "or additional text."
                    "Output:"]
        r["parameters"] = parse_parameters(
            get_response(model, temp_prompt[0]),
            function
            )
        print(f"\r{index}/{len(prompt_list)}" , end="")
    print()
    return res_json
