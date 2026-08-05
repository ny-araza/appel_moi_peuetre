from llm_sdk import Small_LLM_Model

if __name__ == "__main__":
    model = Small_LLM_Model()
    prompt = "1 + 1 ="
    input_ids = model.encode(prompt).tolist()[0]
    logits = model.get_logits_from_input_ids(input_ids)
