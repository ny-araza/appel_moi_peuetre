from typing import Any
import json
import os

def parse(arguments: list[str]) -> dict[str, Any]:
    res: dict[str, Any] = {}
    current_dir = os.path.abspath(os.getcwd())
    function_calling_path: str = os.path.join(
        current_dir, "data/input/function_calling_tests.json"
    )
    function_definition_path: str = os.path.join(
        current_dir, "data/input/functions_definition.json"
    )
    output_path_dir: str = os.path.join(current_dir, "data/output")
    cpt_option: int = 0

    res = {
        "functions_definition": function_definition_path,
        "input": function_calling_path,
        "output": output_path_dir
    }

    if len(arguments) > 6:
        raise Exception (
            "Arguments must be : "
            "   --function_definition <function_calling_path>"
            "   --input <input_path>"
            "   --output <output_path>"
        )

    for i in range(0, len(arguments)):
        if "--" in arguments[i]:
            if arguments[i] == '--input' and arguments[i + 1]:
                res.update({"input": arguments[i + 1]})
            elif arguments[i] == '--output' and arguments[i + 1]:
                res.update({"output": arguments[i + 1]})
            elif arguments[i] == '--function_definition' and arguments[i + 1]:
                res.update({"function_definition": arguments[i + 1]})
            cpt_option += 1

    if arguments and cpt_option > 3:
        raise Exception (
                    "Arguments must be : "
                    "   --function_definition <function_calling_path>"
                    "   --input <input_path>"
                    "   --output <output_path>"
        )

    return res

def read_file(file: str) -> list[dict[Any, Any]]:
    data: list[dict[Any, Any]] = []

    with open(file) as fd:
        data = json.load(fd)

    return data
