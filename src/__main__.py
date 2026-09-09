from .utils import get_function_name  # type: ignore
from llm_sdk import Small_LLM_Model  # type: ignore
import sys
from .parse import parse  # type: ignore
from .output import generate_json_file  # type: ignore


if __name__ == "__main__":
    try:
        model = Small_LLM_Model()
        config = parse(sys.argv[1:])
        result = get_function_name(model, config)
        generate_json_file(config["output"], result)
    except Exception as e:
        print(f"An error occured: {e}")
