from .utils import get_function_name
from llm_sdk import Small_LLM_Model
import sys
from .parse import parse
from .output import generate_json_file
import json

if __name__ == "__main__":
    try:
        model = Small_LLM_Model()
        config = parse(sys.argv[1:])
        result = get_function_name(model, config)
        generate_json_file(config["output"], result)
    except Exception as e:
        print(f"An error occured: {e}")
