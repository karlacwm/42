import numpy as np
from src.llm_manager import LLMManager
from src.schema import FunctionDef


def generate_constrained_deco(
        prompt: str, llm: LLMManager, func: list[FunctionDef],
        max_tokens: int = 10) -> str:
    """Generates text purely by picking the most likely next token."""
    print(f"\nOriginal Prompt: '{prompt}'")

    input_ids: list[int] = llm.text_to_token_ids_list(prompt)
    generated_text = ""

    valid_paths = [f'{{"name":"{f.name}","parameters":{{' for f in func]

    for step in range(max_tokens):
        logit_list = llm.get_logits_list(input_ids)
        logits = np.array(logit_list)
        mask = np.full_like(logits, -np.inf)

        matched_path = None
        for path in valid_paths:
            if generated_text.startswith(path):
                matched_path = path
                break

        if not matched_path:
            possible_paths = [
                p for p in valid_paths if p.startswith(generated_text)]

            for token_id, token_string in llm.id_to_token.items():
                clean_token = token_string.replace("Ġ", "").replace(" ", "")
                if clean_token and any(p.startswith(
                        generated_text + clean_token) for p in possible_paths):
                    mask[token_id] = 0
        else:
            if generated_text.count('{') == 2 and generated_text.count('}') == 1:
                for token_id, token_string in llm.id_to_token.items():
                    if token_string.replace("Ġ", "").replace(" ", "") == "}":
                        mask[token_id] = 0

            else:
                func_name = matched_path.split('"name":"')[1].split('"')[0]
                selected_func = next(f for f in func if f.name == func_name)

                allowed_chars = set('":,.}')
                allowed_chars.update('0123456789-')

                for param_name in selected_func.parameters.keys():
                    allowed_chars.update(param_name)

                for token_id, token_string in llm.id_to_token.items():
                    clean_token = token_string.replace(
                        "Ġ", "").replace(" ", "")

                    if clean_token and all(c in allowed_chars for c in clean_token):
                        if '}' in clean_token and clean_token != '}':
                            continue

                        mask[token_id] = 0

        logits = logits + mask
        best_token_id = int(np.argmax(logits))
        input_ids.append(best_token_id)

        new_word_piece = llm.token_id_to_string(best_token_id)
        generated_text += new_word_piece.replace("Ġ", "").replace(" ", "")
        print(
            f"Step {step+1}: Added token {best_token_id}"
            f" -> '{new_word_piece}'")
        open_brackets = generated_text.count('{')
        close_brackets = generated_text.count('}')

        if open_brackets > 0 and open_brackets == close_brackets:
            print(
                "\nStopping")
            break

    return generated_text
