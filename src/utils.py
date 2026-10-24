from typing import Any
import json
import time

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

def print_token_by_token(data: str) -> None:
    temp = data.split(" ")

    for token in temp:
        print(token, end=" ", flush=True)
        time.sleep(0.05)

    print()
