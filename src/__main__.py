"""The main file of the program."""
try:
    try:
        from .parse import parse
        import sys
        from llm_sdk import Small_LLM_Model  # type: ignore
        from .input import check_input
        from .processing import process
    except KeyboardInterrupt:
        raise KeyboardInterrupt("Operation aborted")
    except Exception as e:
        raise Exception(e)

    if __name__ == "__main__":
        try:
            model = Small_LLM_Model()
            config = parse(sys.argv[1:])
            if check_input(config):
                process(model, config)
        except KeyboardInterrupt:
            raise KeyboardInterrupt("Operation aborted")
        except Exception as e:
            raise Exception(e)
except KeyboardInterrupt as e:
    print(f"{e}")
except Exception as e:
    print(f"An error occured: {e}")
