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
    temp_func_ids = functions_ids[:]
    while prompt and i < get_max_func_len(temp_func_ids):
        logits = model.get_logits_from_input_ids(input_ids)
        logits, functions_ids = check_func_in_logits(logits, functions_ids, i, model)
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
        function_index: int,
        model: Small_LLM_Model
        ) -> tuple[list[float], list[list[int]]]:


    for i in range(len(logits)):
        logits[i] = float("-inf")

    max_token = logits.index(max(logits))
    print(f"max_token = {model.encode(max_token)}")
    # if function_ids:
    for i in range(len(function_ids)):
        print(i)
        print(f"function_ids = {function_ids[i][function_index]}, len = {len(function_ids)}")
        print(f"index = {function_index}")
        if max_token != function_ids[i][function_index]:
            function_ids.pop(i)
        else:
            logits[max_token] = float("+inf")
    return (logits, function_ids)

# logits = [-inf]
# index =  [0,1,2,3,4,5,6,7,8]
# fun_ids = [[0,3,5], [0,6,8,1], [0,9,5,3]]
# res = [0,6,8,1]
# fun_index = 0
# max_token = 0
# func_temp = fun_ids
# ******************************* #

# max_token == func_ids[0][0] oui
# max_token == fun_ids[1][0] oui
# max_token == fun_ids[2][0] oui
# logits[max_token] = +inf
# ******************************* #
# max_token = 6
# fun_index = 1
# max_token == fun_ids[0][1] non
# func_temp.pop(0) => func_temp = [[0,6,8,1], [0,9,5,3]]
# max_token == fun_ids[1][1] oui
# max_token == fun_ids[2][1] non
# func_temp.pop(2) => func_temp = [[0,6,8,1]]

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
             f"The prompt is: {prompt_list[0]["prompt"]}\n"\
             "The function name is : "

    print(get_response(model, prompt, all_function_name))
