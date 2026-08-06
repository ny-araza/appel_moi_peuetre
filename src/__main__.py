import sys
from .parse import parse, read_file
import os

if __name__ == "__main__":
    try:
        config = parse(sys.argv[1:])
        print(read_file(config["functions_definition"]))
    except Exception as e:
        print(f"An error occured: {e}")
