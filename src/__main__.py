from .utils import encode_functions_name
from llm_sdk import Small_LLM_Model
import sys
from .parse import parse


if __name__ == "__main__":
    try:
        model = Small_LLM_Model()
        config = parse(sys.argv[:1])
        encode_functions_name(model, config)
    except Exception as e:
        print(f"An error occured: {e}")
