import sys
from .parse import parse, read_file
import os
from llm_sdk import Small_LLM_Model

if __name__ == "__main__":
    try:
        config = parse(sys.argv[1:])
        model = Small_LLM_Model()
        prompt = "2 + 2 = "
        input_ids = model.encode(prompt)
        logits = model.get_logirom_input_ids(input_ids)
        print(logits)

    except Exception as e:
        print(f"An error occured: {e}")
