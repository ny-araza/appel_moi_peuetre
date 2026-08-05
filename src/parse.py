from typing import Any
import json

def get_input(argument: list[str]) -> None:
    if "--" in argument:
        print(argument.index("-"))

def read_file(file: str) -> list[dict[Any, Any]]:
    data: list[dict[Any, Any]] = []

    with open(file) as fd:
        data = json.load(fd)

    return data
