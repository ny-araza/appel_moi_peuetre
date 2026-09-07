from llm_sdk import Small_LLM_Model
from typing import Any


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
    while prompt and i < 60:
        logits = model.get_logits_from_input_ids(input_ids)
        max_token = max(logits)
        token = logits.index(max_token)
        input_ids.append(token)
        temp_res += model.decode([token])
        i += 1
    return temp_res


def get_length_parameters(function: dict[Any, Any]) -> int:
    pass


def get_parameters(
        model: Small_LLM_Model, 
        res_json: list[dict[Any, Any]],
        list_functions: list[dict[Any, Any]]
        ) -> None:


    function = {}
    print(res_json)
    # for item in list_functions:
    #     if item["name"] == res_json[8]["name"]:
    #         function.update(item)

    # temp_prompt = f"You are a function calling argument extraction agent."\
    #             "Your task is to extract the arguments needed to call the function..\n"\
    #             f"FUNCTION: {function["name"]}\n"\
    #             f"{function["description"]}"\
    #             f"Function parameters: {function["parameters"]}\n User request: {res_json[8]["prompt"]} "\
    #             "Rules:\n"\
    #             "Extract ONLY parameters that are defined in the function parameters.\n"\
    #             "Match information from the user request to the corresponding parameter."\
    #             "Do NOT invent, guess, or infer values that are not explicitly provided."\
    #             "If a required parameter is not provided, set its value to null."\
    #             "Ignore information that is not relevant to the function."\
    #             "Preserve the value exactly as given by the user whenever possible."\
    #             "Return ONLY a JSON object containing the parameter names and their values."\
    #             "Do not add explanations, comments, or additional text."\
    #             "Output:"\
    #             "{'name': 'value'}"
    # print(get_response(model, temp_prompt))
