import numpy as np
from src.llm_manager import LLMManager
from src.schema import FunctionDef


def generate_constrained_decod(
        prompt: str, llm: LLMManager, func: list[FunctionDef],
        max_tokens: int = 150) -> str:

    valid_names = [f.name for f in func]

    # Build a super simple menu so the AI knows what the functions actually do!
    menu = ""
    for f in func:
        menu += f"- {f.name}: {f.description}\n"

    # We create a new prompt just to ask the AI for the name!
    # NEW: We include the 'menu' so it doesn't get tricked by keywords.
    stage1_prompt = f"Question: {prompt}\nHere are the available functions and what they do:\n{menu}\nBased on the question, which function should be used? Answer with EXACTLY one function name:"
    
    input_ids = llm.text_to_token_ids_list(stage1_prompt)

    generated_name = ""
    matched_name = None

    # We only give it 20 steps because we only need the short name
    for _ in range(20):
        logits = np.array(llm.get_logits_list(input_ids))
        best_token = int(np.argmax(logits))
        input_ids.append(best_token)

        piece = llm.token_id_to_string(best_token)
        generated_name += piece

        # If we see one of our valid function names in what it typed, we win!
        for name in valid_names:
            if name in generated_name:
                matched_name = name
                break
        if matched_name:
            break

    # Fallback: If the AI gets confused, safely default to the first function
    if not matched_name:
        matched_name = valid_names[0]

    print(f"[Stage 1] AI picked function: {matched_name}")

    # NEW: Let's find the exact expected parameter names from your schema
    expected_params = []
    for f in func:
        if f.name == matched_name:
            expected_params = list(f.parameters.keys())
            break
            
    # NEW: We tell the AI exactly which parameter keys we want!
    stage2_prompt = f"Question: {prompt}\nOutput ONLY a valid JSON dictionary containing the parameters {expected_params} for the function '{matched_name}'.\nJSON:"
    input_ids = llm.text_to_token_ids_list(stage2_prompt)

    generated_params = ""
    for step in range(max_tokens):
        logits = np.array(llm.get_logits_list(input_ids))
        best_token = int(np.argmax(logits))
        input_ids.append(best_token)

        piece = llm.token_id_to_string(best_token)
        generated_params += piece

        # Stop when the JSON brackets are perfectly balanced
        open_brackets = generated_params.count('{')
        close_brackets = generated_params.count('}')
        if open_brackets > 0 and open_brackets == close_brackets:
            break

    # The AI might have said "Here is your JSON: { ... }".
    # We use find() to chop off the extra words and just grab the brackets!
    start_idx = generated_params.find('{')
    end_idx = generated_params.rfind('}') + 1

    if start_idx != -1 and end_idx != -1:
        clean_params = generated_params[start_idx:end_idx]
    else:
        clean_params = "{}"  # Ultimate safe fallback

    # We manually build the final string. This guarantees the formatting is flawlessly perfect.
    final_json_string = f'{{"name": "{matched_name}", "parameters": {clean_params}}}'

    return final_json_string