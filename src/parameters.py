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
        t = model.decode([token])
        print(t)
        if t == "}\n\n" or t == "\"}\n\n":
            break
        input_ids.append(token)
        i += 1
    print(temp_res)
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
    print(parameters.strip(" Answer"))
    temp_params = json.loads(parameters.strip(" Answer"))
    print(temp_params)

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
            if type_parameters[key]["type"] == "bool":
                parameters.update({key: value.strip().lower() == "true"})
        else:
            parameters.update({key: None})
    # print("cast_parameters (parameters) => ", parameters)
    return parameters


def get_parameters(
        model: Small_LLM_Model,
        res_json: list[dict[Any, Any]],
        list_functions: list[dict[Any, Any]]
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
    for r in res_json:
        for item in list_functions:
            if item["name"] == r["name"]:
                function.update(item)

        temp_prompt = [
                    f"""You are a function-calling argument extractor.
                    Output ONE JSON object and nothing else: no explanation, no comments, no markdown fences.

                    Function: {function['name']}
                    Description: {function['description']}
                    Parameters (JSON schema):
                    {json.dumps(function['parameters'], indent=2)}

                    Rules:
                    - Output one key for EVERY parameter listed above, and no other keys.
                    - Take values only from the user request. Never invent or infer.
                    - If a value is not explicitly stated, use null.
                    - Copy values exactly as the user wrote them. Respect the declared type.
                    - Ignore anything in the request that maps to no parameter.

                    Example
                    Function: fn_read_file
                    Parameters: {{"path": {{"type": "string"}}, "encoding": {{"type": "string"}}}}
                    User request: Read /var/log/app.log for me
                    Output: {{"path": "/var/log/app.log", "encoding": null}}

                    Function: {function['name']}
                    Parameters: {list(function['parameters'].keys())}
                    User request: {r['prompt']}
                    Output:"""]
        print("r => ", r)
        # r["parameters"] = parse_parameters(
        #     get_response(model, temp_prompt[0]),
        #     function
        #     )
        r["parameters"] = get_response(model, temp_prompt[0])
    return res_json
