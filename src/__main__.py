from llm_sdk import Small_LLM_Model

if __name__ == "__main__":
    model = Small_LLM_Model()
    prompt = ""
    input_ids = model.encode(prompt).tolist()[0]
    i = 0
    while prompt and i < 20:
        logits = model.get_logits_from_input_ids(input_ids)
        max_token = max(logits)
        token = logits.index(max_token)
        input_ids.append(token)
        print(model.decode([token]))
        i += 1
