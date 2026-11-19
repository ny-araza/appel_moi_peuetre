"""All function to retrieve the function name."""

from llm_sdk import Small_LLM_Model  # type: ignore
from typing import Any
from .utils import read_file


def get_max_func_len(functions_name: list[list[int]]) -> int:
    """Get the max lentgh of the function name.

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


def search_func_name(
    logits: list[float],
    function_ids: list[list[int]],
    res: list[int],
    function_found: bool = False
) -> tuple[list[float], list[list[int]], list[int], bool]:
    """Found the function name inside the functions definitions.

    Args:
        function_ids (list[list[int]]): List of the function name encoded
        res (list[int]): list of the max_token
        function_found (bool): check if the function name is found or not

    Returns:
        tuple[
            list[float],
            list[list[int]],
            list[int],
            bool
        ]: Update the logits, update the function name ids,
        update the res, update the function_foun
    """
    valid_tokens = set()

    for func in function_ids:
        if len(res) < len(func) and func[:len(res)] == res:
            valid_tokens.add(func[len(res)])

    if not valid_tokens:
        function_found = True
        return logits, function_ids, res, function_found

    max_token = max(valid_tokens, key=lambda token: logits[token])

    for i in range(len(logits)):
        if i not in valid_tokens:
            logits[i] = float("-inf")

    res.append(max_token)

    return logits, function_ids, res, function_found


def get_response(
        model: Small_LLM_Model,
        prompt: str,
        functions_ids: list[list[int]],
        functions_name: list[str]
        ) -> str:
    """Get the response from LLM (its return the function name).

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
    function_found: bool = False
    while i <= get_max_func_len(functions_ids) + 1:
        logits = model.get_logits_from_input_ids(input_ids)
        logits, functions_ids, res, function_found = search_func_name(
            logits, functions_ids, res, function_found
            )
        if function_found:
            break
        max_token = max(logits)
        token = logits.index(max_token)
        input_ids.append(token)
        temp_res += model.decode([token])
        i += 1
    return temp_res


def get_function_name(
        model: Small_LLM_Model,
        config: dict[str, Any],
        prompt: str
        ) -> str:
    """Get all the function name from each prompt.

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
