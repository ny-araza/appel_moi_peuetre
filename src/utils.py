import sys
from llm_sdk import Small_LLM_Model
from .parse import parse, read_file
from typing import Any

def get_response(model: Small_LLM_Model, prompt: str):
    input_ids = model.encode(prompt).tolist()[0]
    i = 0
    while prompt and i < 20:
        logits = model.get_logits_from_input_ids(input_ids)
        max_token = max(logits)
        token = logits.index(max_token)
        input_ids.append(token)
        print(model.decode([token]), end="")
        i += 1


def encode_prompt(prompt: str, model: Small_LLM_Model) -> None:
     input_ids = model.encode(prompt).tolist()[0]
     return input_ids


def get_max_func_len(tab: list[list[int]]) -> int:
    length_tab = []
    for l in tab:
        length_tab.append(len(l))
    return max(l)


def encode_functions_name(model: Small_LLM_Model, config: dict[str, Any]) -> None:
    functions_definition = read_file(config["functions_definition"])
    prompt_list = read_file(config["input"])
    str_form = []
    for function in functions_definition:
        str_form.append(f"{function["name"]}: {function["description"]}")

    var = '\n'.join(str_form)

    prompt = "You are going to treat the following prompt by function " \
             "calling. Choose one from the functions name with its " \
             f"description listed below to answer the prompt:\n{var}\n" \
             f"The prompt is: {prompt_list[0]["prompt"]}\n"\
             "The function name is : "    

    get_response(model, prompt)
