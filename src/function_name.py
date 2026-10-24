from llm_sdk import Small_LLM_Model
from typing import Any
from .utils import read_file


def parse_res(res: str, functions_name: list[str]) -> str:
    """Trim the llm response

        Args:
            res (str): The llm response

        Returns:
            str: The value after trimed
    """
    forbidden_character = "!*/?@"
    new_res: str = ""
    for c in res:
        if c in forbidden_character:
            c = c.replace(c, "")
        new_res += c
    temp = new_res.split("fn")
    if len(temp) > 2:
        new_res = f"fn{temp[1]}"
    if new_res[-2:] == "fn":
        return new_res[:-2]
    return trim_functions_name(new_res, functions_name)


def trim_functions_name(old_name: str, functions_name: list[str]) -> str:
    if not old_name:
        return "not_found"
    temp_old = old_name
    if "fn" in old_name:
        temp_old = old_name.split("fn")[1].strip("_ ")
    
    for func_name in functions_name:
        if "fn" in func_name:
            temp_fun_name = func_name.split("fn")[1].strip("_ ")
            if temp_fun_name == temp_old:
                return func_name
        else:
            if temp_old in func_name:
                return func_name
    return old_name


def get_max_func_len(functions_name: list[list[int]]) -> int:
    """Get the max lentgh of the function name

        Args:
            functions_name (list[list[int]]): List of the function name

        Returns:
            int: the max length between all the function name
    """
    length_tab = []
    for func in functions_name:
        if not func:
            raise ValueError("Function must have a name")
        length_tab.append(len(func))
    return max(length_tab)


def check_func_in_logits(
        logits: list[float],
        function_ids: list[list[int]],
        res: list[int],
        ) -> tuple[
            list[float],
            list[list[int]],
            list[int],
            ]:
    """Guide the llm to return only the function name

        Args:
            logits (list[float]): the llm logits listpositional arguments,
            return the largest argument.
            function_ids (list[list[int]]): numeric representation
            of the function name
            res (list[int]): The function name returned

        Returns:
            tuple[
            list[float],
            list[list[int]],
            list[int]: return the logits, the function_ids
            and the res (function name)
    """
    max_token = logits.index(max(logits))
    for i in range(len(logits)):
        logits[i] = float("-inf")

    if res in function_ids:
        return (logits, function_ids, res)
    for item in function_ids:
        if max_token in item:
            res.append(max_token)
            logits[max_token] = float("+inf")
    return (logits, function_ids, res)

def get_response(
        model: Small_LLM_Model,
        prompt: str,
        functions_ids: list[list[int]],
        functions_name: list[str]
        ) -> str:
    """Get the response from LLM (its return the function name)

        Args:
            model (Small_LLM_Model): The llm model
            prompt (str): The prompt send to the llm
            functions_ids: Numeric Representations of all the functions

        Returns:
            str: The function name
    """
    input_ids = model.encode(prompt).tolist()[0]
    i = 0
    temp_res = ""
    res: list[int] = []
    while i <= get_max_func_len(functions_ids) + 1:
        logits = model.get_logits_from_input_ids(input_ids)
        logits, functions_ids, res = check_func_in_logits(
            logits, functions_ids, res
            )
        max_token = max(logits)
        token = logits.index(max_token)
        input_ids.append(token)
        temp_res += model.decode([token])
        i += 1
        print(temp_res, end="")
    return parse_res(temp_res, functions_name)


def get_function_name(
        model: Small_LLM_Model,
        config: dict[str, Any],
        prompt: str
        ) -> str:
    """Get all the function name from each prompt

        Args:
            model (Small_LLM_Model): The LLM model
            config (dict[str, Any]): The input value in a dict

        Returns:
            list[dict[Any, Any]]: The output value
    """
    functions_definition = read_file(config["functions_definition"])
    str_form = []
    all_function_name_ids = []
    all_function_name: list[str] = []
    for function in functions_definition:
        all_function_name.append(function["name"])
        str_form.append(f"{function["name"]}: {function["description"]}")
        input_ids = model.encode(function["name"]).tolist()[0]
        all_function_name_ids.append(input_ids)

    # prompt_list = read_file(config["input"])
    # for prompt in prompt_list:
    #     if not prompt["prompt"].strip(" \t\n\a\b\v\f\r"):
    #         raise Exception("Prompt not valid")

    var = '\n'.join(str_form)
    
    temp_prompt = f"""
        Select one function by matching the user's 
        intent to the function descriptions.
        Functions:
        {var}
        User request: <request>{prompt}</request>
        Return only the exact function name 
        whose description is the best match. 
        Do not explain. Never invent a function name.
        Answer: 
        """.strip()

    return get_response(
        model, temp_prompt,
        all_function_name_ids,
        all_function_name
    )



