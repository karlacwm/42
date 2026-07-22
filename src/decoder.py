import numpy as np
from src.llm_manager import LLMManager


def generate_unconstrained(
        prompt: str, llm: LLMManager, max_tokens: int = 20) -> str:
    """Generates text purely by picking the most likely next token."""
    print(f"\nOriginal Prompt: '{prompt}'")

    input_ids: list[int] = llm.text_to_token_ids_list(prompt)
    generated_text = ""

    for step in range(max_tokens):
        # 1. Get probabilities
        logit_list = llm.get_logits_list(input_ids)
        logits = np.array(logit_list)
        if step == 0:
            mask = np.full_like(logits, -np.inf)

            for token_id, token_string in llm.id_to_token.items():
                # We use .strip() to catch "{" and " {" (with spaces)
                if token_string.replace("Ġ", "").strip() == "{":
                    mask[token_id] = 0

            # Apply our mask to the AI's scoreboard
            # (Any normal score + (-inf) = -inf. The AI is now powerless!)
            logits = logits + mask

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
