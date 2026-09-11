from llm_sdk import Small_LLM_Model  # type: ignore
from typing import Any


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
        if "}" in temp:
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
    forbidden_character = " +-&%!*/?@\n'`"
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
    """Cast the value of parameters
    
        Args:
            parameters (str): the LLM response that will be trim
            function (dict[Any, Any]): The function

        Returns:
            dict[Any, Any]: The parameters dict with all value casted
    """
    type_parameters = function["parameters"]
    for item in parameters.items():
        if not type_parameters[item[0]]["type"]:
            raise ValueError("Parameter must have a value")
        if type_parameters[item[0]]["type"] == "number":
            parameters.update({item[0]: float(item[1])})
        if type_parameters[item[0]]["type"] == "bool":
            parameters.update({item[0]: item[1].strip().lower() == "true"})
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
                    f"You are a function calling argument extraction agent."
                    "Your task is to extract the arguments needed "
                    "to call the function..\n"
                    f"FUNCTION: {function["name"]}\n"
                    f"{function["description"]}"
                    f"Function parameters: {function["parameters"]}\n "
                    f"User request: {r["prompt"]}"
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
    return res_json
