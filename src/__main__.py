from .parse import parse
import sys
from llm_sdk import Small_LLM_Model
from .input import check_input
from .processing import process


if __name__ == "__main__":
    model = Small_LLM_Model()
    config = parse(sys.argv[1:])
    if check_input(config):
        process(model, config)
