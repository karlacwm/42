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
        
        if generated_text in valid_paths:
            # STATE 4: Parameters! (We turn off the bouncer here for now)
            mask = np.zeros_like(logits)
        else:
            # Find which paths are still possible based on what we've generated
            possible_paths = [
                p for p in valid_paths if p.startswith(generated_text)]

            for token_id, token_string in llm.id_to_token.items():
                clean_token = token_string.replace("Ġ", "").replace(" ", "")
                if not clean_token:
                    continue

                test_string = generated_text + clean_token

                # If this token keeps us on ANY valid path, unban it!
                if any(p.startswith(test_string) for p in possible_paths):
                    mask[token_id] = 0

        logits = logits + mask
        best_token_id = int(np.argmax(logits))
        input_ids.append(best_token_id)

        new_word_piece = llm.token_id_to_string(best_token_id)
        generated_text += new_word_piece.replace("Ġ", "").replace(" ", "")
        print(
            f"Step {step+1}: Added token {best_token_id}"
            f" -> '{new_word_piece}'")
        if generated_text.endswith("}}"):
            print("\n == reached the }} ")
            break

    return generated_text
