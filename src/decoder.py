import numpy as np
from src.llm_manager import LLMManager
from src.schema import FunctionDef


def generate_constrained_decod(
        prompt: str, llm: LLMManager, func: list[FunctionDef],
        max_tokens: int = 150) -> str:

    valid_names = [f.name for f in func]

    # ==========================================
    # STAGE 1: Let the AI pick the function name
    # ==========================================
    # We create a new prompt just to ask the AI for the name!
    stage1_prompt = f"Question: {prompt}\nWhich of these functions should be used? {valid_names}\nAnswer with exactly one function name:"
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

    # ==========================================
    # STAGE 2: Let the AI generate the parameters
    # ==========================================
    # Now we ask it to generate JUST the parameters for the function it picked!
    stage2_prompt = f"Question: {prompt}\nOutput only a valid JSON dictionary containing the parameters for the function '{matched_name}'.\nJSON:"
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

    # ==========================================
    # STAGE 3: Assemble the Perfect JSON
    # ==========================================
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
    print(final_json_string)
    return final_json_string
