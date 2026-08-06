import sys
from .parse import parse

if __name__ == "__main__":
    try:
        parse(sys.argv[1:])
    except Exception as e:
        print(f"An error occured: {e}")
