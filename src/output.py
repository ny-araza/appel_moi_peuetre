from typing import Any
import json
from pydantic import BaseModel, TypeAdapter, ValidationError
import os


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
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])
        return False


def generate_json_file(filename: str, res_json: list[dict[Any, Any]]) -> None:
    outputpath: str = ""
    if (validate_json(res_json)):
        if not os.path.exists(filename):
            if filename.split("/")[-2:] == ["data", "output"]:
                os.mkdir(filename)
            else:
                outputpath = filename
        if os.path.isdir(filename):
            outputpath = os.path.join(
                filename,
                "function_calling_results.json"
                )
        else:
            outputpath = filename
        with open(outputpath, "w") as fd:
            json.dump(res_json, fd, indent=2)
    else:
        raise ValueError("JSON generated not valide")
