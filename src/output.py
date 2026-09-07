from typing import Any
import json

def generate_json_file(filename: str, res_json: list[dict[Any, Any]]) -> None:
    print(json.dump(res_json))