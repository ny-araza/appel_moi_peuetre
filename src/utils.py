from llm_sdk import Small_LLM_Model  # type: ignore
from .parse import read_file
from typing import Any
from .parameters import get_parameters


def get_response(
        model: Small_LLM_Model,
        prompt: str,
        functions_ids: list[list[int]]
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
            model, logits, functions_ids, res
            )
        max_token = max(logits)
        token = logits.index(max_token)
        input_ids.append(token)
        temp_res += model.decode([token])
        i += 1
    return parse_res(temp_res)


def parse_res(res: str) -> str:
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
    return new_res


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
        model: Small_LLM_Model,
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
            logits (list[float]): the llm logits list
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


def get_function_name(
        model: Small_LLM_Model,
        config: dict[str, Any]
        ) -> list[dict[Any, Any]]:
    """Get all the function name from each prompt

        Args:
            model (Small_LLM_Model): The LLM model
            config (dict[str, Any]): The input value in a dict

        Returns:
            list[dict[Any, Any]]: The output value
    """
    functions_definition = read_file(config["functions_definition"])
    prompt_list = read_file(config["input"])
    str_form = []
    all_function_name = []
    result: list[dict[Any, Any]] = []
    for function in functions_definition:
        str_form.append(f"{function["name"]}: {function["description"]}")
        input_ids = model.encode(function["name"]).tolist()[0]
        all_function_name.append(input_ids)

    var = '\n'.join(str_form)
    print("Get the function name:")
    for i, prompt in enumerate(prompt_list, 1):
        temp_prompt = [
                "You are a function-calling selection system.\n"
                "Below is the list of available functions, with their "
                "exact name and description:\n\n"
                f"{var}\n\n"
                "Strict instructions:\n"
                "1. Read the user's request below.\n"
                "2. Choose ONE SINGLE function from the list, the one that "
                "best matches the request.\n"
                "3. Reply ONLY with the exact function name, "
                "copied as-is from the list (respect spelling and the "
                "'fn_' prefix).\n"
                "4. Do not add any explanation, punctuation, or extra words.\n"
                "5. Never answer with a full sentence, "
                "only the function name.\n\n"
                "Examples:\n"
                "Request: \"What is 12 times 4?\"\n"
                "Answer: fn_multiply_numbers\n\n"
                "Request: \"Is 17 an even number?\"\n"
                "Answer: fn_is_even\n\n"
                f"Request: \"{prompt['prompt']}\"\n"
                "Answer:"
            ]

        function_name = get_response(model, temp_prompt[0], all_function_name)
        print(f"\r{i}/{len(prompt_list)} ...", end="")
        if not function_name:
            result.append(
                {
                            "prompt": prompt["prompt"],
                            "name": "not_found",
                            "parameters": {}
                }
            )
            continue
        result.append(
            {
                "prompt": prompt["prompt"],
                "name": function_name,
                "parameters": {}
            }
        )
    print()
    result = get_parameters(model, result, functions_definition, prompt_list)
    return result
