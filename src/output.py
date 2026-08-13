from llm_sdk import Small_LLM_Model

def parse_output() -> None:
    model = Small_LLM_Model()
    logits_begin_json = model.decode([90])
    prompt = "What is the sum of 40 and 2?"
    input_ids = model.encode(prompt).tolist()[0]
    i = 0
    while i < 60:
        logits = model.get_logits_from_input_ids(input_ids)
        print(model.decode(logits.index(max(logits))), end=" ")
        input_ids.append(logits.index(max(logits)))
        i += 1

# prompt = Instruction + description + nom_fonction + prompt
# 1. encode(function_name) => [0,1,3], [0,3,2]
# 2. encode_prompt => [12,5,4,..,3,2]
# 3. res = 0
# 4. si res = "" => check si 0 est dans encode_prompt si oui mettre tous les elements sauf 0 e -inf
# et incrementer la boucle
# 
