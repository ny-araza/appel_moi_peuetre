from typing import Any
import json
from pydantic import BaseModel, TypeAdapter



class Output(BaseModel):
    prompt: str
    name: str
    parameters: dict[Any, Any]


def validate_json(res_json: list[dict[Any, Any]]) -> bool:
    Output.model_validate_json(str(res_json))


def generate_json_file(filename: str, res_json: list[dict[Any, Any]]) -> None:
    with open(filename, "w") as fd:
        json.dump(res_json, fd,indent=2)
