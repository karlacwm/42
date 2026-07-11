import numpy as np
from typing import List
from src.llm_manager import LLMManager


def generate_unconstrained(
        prompt: str, llm: LLMManager, max_tokens: int = 20) -> str:
    """Generates text purely by picking the most likely next token."""
    print(f"\nOriginal Prompt: '{prompt}'")
    print("Model is generating text...")

    input_ids: List[int] = llm.text_to_token_ids_list(prompt)
    generated_text = ""

    for step in range(max_tokens):
        # 1. Get probabilities
        logits = llm.get_logits_list(input_ids)

        # 2. Pick the highest scoring token
        best_token_id = int(np.argmax(logits))

        # 3. Add to sequence
        input_ids.append(best_token_id)

        # 4. Map back to text
        new_word_piece = llm.token_id_to_string(best_token_id)
        generated_text += new_word_piece

        print(
            f"Step {step+1}: Added token {best_token_id}"
            f" -> '{new_word_piece}'")

    return generated_text
