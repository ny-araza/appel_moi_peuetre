from typing import Any
import json
from pydantic import BaseModel, TypeAdapter, ValidationError
import json

class Output(BaseModel):
    prompt: str
    name: str
    parameters: dict[Any, Any]


def validate_json(res_json: list[dict[Any, Any]]) -> bool:
    try:
        json_parse = json.dumps(res_json)
        adapter = TypeAdapter(list[Output])
        adapter.validate_json(json_parse)
        return True
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])
            return False

def generate_json_file(filename: str, res_json: list[dict[Any, Any]]) -> None:
    if (validate_json(res_json)):
        with open(filename, "w") as fd:
            json.dump(res_json, fd,indent=2)
    else:
        raise ValueError("JSON generated not valide")
