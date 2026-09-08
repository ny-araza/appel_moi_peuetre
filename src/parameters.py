from llm_sdk import Small_LLM_Model
from typing import Any
import json

def check_func_in_logits(
        logits: list[float],
        function_ids: list[list[int]],
        ) -> list[float]:


    max_token = logits.index(max(logits))
    for i in range(len(logits)):
        logits[i] = float("-inf")

    function_set = set()
    for item in function_ids:
        for token in item:
            function_set.add(token)

    if max_token in function_set:
        logits[max_token] = float("+inf")
    return (logits)


def get_response(
        model: Small_LLM_Model, 
        prompt: str,
        ) -> str:
    input_ids = model.encode(prompt).tolist()[0]
    i = 0
    temp_res = ""
    while i < 60:
        logits = model.get_logits_from_input_ids(input_ids)
        max_token = max(logits)
        token = logits.index(max_token)
        temp = model.decode([token])
        temp_res += temp
        if "}" in temp:
            break
        input_ids.append(token)
        i += 1
    return temp_res


def parse_parameters(parameters: str, function: dict[Any, Any]) -> dict[Any, Any]:
    forbidden_character = " +-&%!*/?@\n'"
    res: dict[str, Any] = {}
    temp = ""
    for c in parameters:
        if c in forbidden_character:
            c = c.replace(c, "")
        temp += c
    tmp = temp[1:-1].split(",")
    for t in tmp:
        item = t.split(":")
        res.update({
            item[0].strip("\""): item[1].strip("\"")
        })
    return cast_parameters(res, function)


def cast_parameters(
        parameters: dict[Any, Any], 
        function: dict[Any, Any]
        ) -> dict[Any, Any]:
    type_parameters = function["parameters"]
    for item in parameters.items():
        if type_parameters[item[0]]["type"] == "number":
            parameters.update({item[0]: float(item[1])})
    return parameters


def get_parameters(
        model: Small_LLM_Model, 
        res_json: list[dict[Any, Any]],
        list_functions: list[dict[Any, Any]]
        ) -> list[dict[Any, Any]]:


    function = {}
    for r in res_json:
        for item in list_functions:
            if item["name"] == r["name"]:
                function.update(item)

        temp_prompt = "You are a function argument extraction agent. Extract parameters strictly using the provided context:" \
                        f"FUNCTION: {function["name"]}\n" \
                        f"DESCRIPTION : {function["description"]}\n" \
                        f"PARAMETERS:: {function["parameters"]}\n" \
                        f"USER REQUEST : {r["prompt"]}\n" \
                    """Rules::
                        1. Extract ONLY parameters defined in the function.
                        2. Do NOT invent, guess, or infer values.
                        3. Set missing required parameters to null.
                        4. Preserve exact user values.
                        5. Output ONLY a valid JSON object: {"param_name": "value"}. No explanations or extra text.
                        Output:
                    """

        r["parameters"] = parse_parameters(get_response(model, temp_prompt), function)
    return res_json
