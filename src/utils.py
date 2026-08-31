import sys
from llm_sdk import Small_LLM_Model
from .parse import parse, read_file
from typing import Any

def get_response():
    model = Small_LLM_Model()
    prompt = ""
    input_ids = model.encode(prompt).tolist()[0]
    i = 0
    while prompt and i < 20:
        logits = model.get_logits_from_input_ids(input_ids)
        max_token = max(logits)
        token = logits.index(max_token)
        input_ids.append(token)
        print(model.decode([token]))
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
    input_prompt_ids = encode_prompt(prompt_list[0]["prompt"], model)
    res = []
    for item in functions_definition:
        input_ids = model.encode(item["name"]).tolist()[0]
        if not res:
            res.append(input_ids[0])
        else:
            pass
