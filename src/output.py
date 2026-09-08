from typing import Any
import json
from pydantic import BaseModel, TypeAdapter



class Output(BaseModel):
    prompt: str
    name: str
    parameters: dict[Any, Any]


def validate_output(res_json: list[dict[Any, Any]]) -> bool:
    pass

def generate_json_file(filename: str, res_json: list[dict[Any, Any]]) -> None:
    # adapter = TypeAdapter(list[Output])
    print(json.dumps(res_json, indent=2))
    # adapter.validate_json(str(res_json))
