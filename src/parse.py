from typing import Any
import json
import os


def check_flag_valid(argv: list[str]) -> bool:
    """Check if the flag in input is allowed
    (--input, --output ,--function_definition)

        Args:
            argv (list[str]): The input flag

        Returns:
            bool: True is the flag is valid and false if its not
    """
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
    """Get all the flag in input and stock with its value in a dict

        Args:
            arguments (list[str]): The input flag

        Returns:
            dict[str, Any]: The flag with its value
    """
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
    flag_authorized = ["--input", "--output", "functions_definition"]
    for i in range(0, len(arguments)):
        if "--" in arguments[i]:
            if arguments[i] == '--input' and arguments[i + 1]:
                res.update({"input": arguments[i + 1]})
            elif arguments[i] == '--output' and arguments[i + 1]:
                res.update({"output": arguments[i + 1]})
            elif arguments[i] == '--functions_definition' and arguments[i + 1]:
                res.update({"functions_definition": arguments[i + 1]})
            elif arguments[i] not in flag_authorized:
                raise Exception(
                    "Flag must be in "
                    f"{flag_authorized}"
                )
            cpt_option += 1
    if output_path_dir != res.get("output"):
        if len(res.get("output", "")) > 0:
            temp = res.get("output", "").split(".")
            if len(temp) != 2 or temp[1].lower() != "json":
                raise Exception("Output file must be a JSON file")
        else:
            raise Exception("Output must have a value")
    if function_calling_path != res.get("input"):
        if len(res.get("input", "")) > 0:
            temp = res.get("input", "").split(".")
            if len(temp) != 2 or temp[1].lower() != "json":
                raise Exception("input file must be a JSON file")
        else:
            raise Exception("Output must have a value")
    if function_definition_path != res.get("functions_definition"):
        if len(res.get("functions_definition", "")) > 0:
            temp = res.get("functions_definition", "").split(".")
            if len(temp) != 2 or temp[1].lower() != "json":
                raise Exception(
                    "functions_definition "
                    "file must be a JSON file"
                    )
        else:
            raise Exception("Output must have a value")
    if arguments and cpt_option > 3:
        raise Exception(
            "Arguments must be : "
            "   --functions_definition <function_calling_path>"
            "   --input <input_path>"
            "   --output <output_path>"
        )

    return res


def read_file(file: str) -> list[dict[Any, Any]]:
    """read the JSON file a set it into a varable

        Args:
            file (str): The JSON filepath

        Returns:
            list[dict[Any, Any]]: The JSON read
    """
    data: list[dict[Any, Any]] = []

    with open(file) as fd:
        data = json.load(fd)

    return data
