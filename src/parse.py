from typing import Any
import json


def parse(arguments: list[str]) -> None:
    res: dict[str, Any] = {}
    cpt_input: int = 0
    cpt_output: int = 0
    function_calling_path: str = "/data/input/function_calling_tests.json"
    function_definition_path: str = "/data/input/functions_definition.json"
    output_path_dir: str = "/data/output"

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
                cpt_input += 1
            elif arguments[i] == '--output' and arguments[i + 1]:
                res.update({"output": arguments[i + 1]})
                cpt_output += 1
            elif arguments[i] == '--function_definition' and arguments[i + 1]:
                res.update({"function_definition": arguments[i + 1]})

    print(res)

def read_file(file: str) -> list[dict[Any, Any]]:
    data: list[dict[Any, Any]] = []

    with open(file) as fd:
        data = json.load(fd)

    return data
