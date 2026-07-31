import numpy as np
from src.llm_manager import LLMManager
from src.schema import FunctionDef


def generate_unconstrained(
        prompt: str, llm: LLMManager, func: list[FunctionDef],
        max_tokens: int = 20) -> str:
    """Generates text purely by picking the most likely next token."""
    print(f"\nOriginal Prompt: '{prompt}'")

    input_ids: list[int] = llm.text_to_token_ids_list(prompt)
    generated_text = ""

    for step in range(max_tokens):
        logit_list = llm.get_logits_list(input_ids)
        logits = np.array(logit_list)

        mask = np.full_like(logits, -np.inf)
        name_format = '{"name":"'

        if len(generated_text) < len(name_format):
            remaining = name_format[len(generated_text):]

            for token_id, token_string in llm.id_to_token.items():
                clean_token = token_string.replace("Ġ", "").replace(" ", "")

                if clean_token and remaining.startswith(clean_token):
                    mask[token_id] = 0
        else:
            mask = np.zeros_like(logits)

        logits = logits + mask

        best_token_id = int(np.argmax(logits))

        input_ids.append(best_token_id)

        new_word_piece = llm.token_id_to_string(best_token_id)
        generated_text += new_word_piece.replace("Ġ", "").replace(" ", "")

        print(
            f"Step {step+1}: Added token {best_token_id}"
            f" -> '{new_word_piece}'")

    return generated_text
