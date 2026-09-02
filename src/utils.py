import sys
from llm_sdk import Small_LLM_Model
from .parse import parse, read_file
from typing import Any

def get_response(
        model: Small_LLM_Model, 
        prompt: str, 
        functions_ids: list[list[int]]
        ) -> str:
    input_ids = model.encode(prompt).tolist()[0]
    i = 0
    temp_res = ""
    while prompt and i < get_max_func_len(functions_ids):
        logits = model.get_logits_from_input_ids(input_ids)
        logits = check_func_in_logits(logits, functions_ids)
        max_token = max(logits)
        token = logits.index(max_token)
        input_ids.append(token)
        temp_res += model.decode([token])
        i += 1
    return temp_res


def encode_prompt(prompt: str, model: Small_LLM_Model) -> None:
     input_ids = model.encode(prompt).tolist()[0]
     return input_ids


def get_max_func_len(functions_name: list[list[int]]) -> int:
    length_tab = []
    for l in functions_name:
        length_tab.append(len(l))
    return max(length_tab)


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

# func_ids [[8822, 2891, 32964], [8822, 1889, 3744], [8822, 43277, 3904], [8822, 3062, 39794, 12993], [8822, 5228, 7660, 3904, 6615, 41832]]

def encode_functions_name(model: Small_LLM_Model, config: dict[str, Any]) -> None:
    functions_definition = read_file(config["functions_definition"])
    prompt_list = read_file(config["input"])
    str_form = []
    all_function_name = []

    for function in functions_definition:
        str_form.append(f"{function["name"]}: {function["description"]}")
        input_ids = model.encode(function["name"]).tolist()[0]
        all_function_name.append(input_ids)

    var = '\n'.join(str_form)

    prompt = "You are going to treat the following prompt by function " \
             "calling. Choose one from the functions name with its " \
             f"description listed below to answer the prompt:\n{var}\n" \
             f"The prompt is: {prompt_list[5]["prompt"]}\n"\
             "The function name is : "

    print(get_response(model, prompt, all_function_name))
