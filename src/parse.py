from typing import Any
import json
import os


def check_flag_valid(argv: list[str]) -> bool:
    flag_valid = ["--input", "--output", "--functions_definition"]
    cpt: int = 0
    if len(argv) > 0:
        for argument in argv:
            for flag in flag_valid:
                if argument == flag:
                    cpt += 1
    else:
        return True
    if cpt > 3 or cpt == 0:
        return False
    return True


def parse(arguments: list[str]) -> dict[str, Any]:
    res: dict[str, Any] = {}
    current_dir = os.path.abspath(os.getcwd())
    output_dir = current_dir + "/data/output"
    function_calling_path: str = os.path.join(
        current_dir, "data/input/function_calling_tests.json"
    )
    function_definition_path: str = os.path.join(
        current_dir, "data/input/functions_definition.json"
    )
    output_path_dir: str = output_dir
    cpt_option: int = 0

    res = {
        "functions_definition": function_definition_path,
        "input": function_calling_path,
        "output": output_path_dir
    }
    if not check_flag_valid(arguments) or len(arguments) > 6:
        raise Exception(
            "Arguments must be : "
            "   --functions_definition <function_calling_path>"
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
        raise Exception(
            "Arguments must be : "
            "   --functions_definition <function_calling_path>"
            "   --input <input_path>"
            "   --output <output_path>"
        )

    return res


def read_file(file: str) -> list[dict[Any, Any]]:
    data: list[dict[Any, Any]] = []

    with open(file) as fd:
        data = json.load(fd)

    return data
