try:
    import sys
    from .utils import get_function_name
    from llm_sdk import Small_LLM_Model
    from .parse import parse
    from .output import generate_json_file
    from .input import check_input
except KeyboardInterrupt:
    print("Please wait until the json is generated!!")
except Exception as e:
    print(f"An error occured: {e}")

if __name__ == "__main__":
    try:
        model = Small_LLM_Model()
        config = parse(sys.argv[1:])
        if check_input(config):
            result = get_function_name(model, config)
            generate_json_file(config["output"], result)
            print("Generation json done!!")
    except KeyboardInterrupt:
        print("Please wait until the end!!")
    except Exception as e:
        print(f"An error occured: {e}")
