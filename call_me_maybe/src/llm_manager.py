import json
import sys
from typing import Any
from llm_sdk import Small_LLM_Model  # type: ignore


class LLMManager:
    def __init__(self) -> None:
        try:
            self.model = Small_LLM_Model()
        except Exception as e:
            print(f"Error occurred: {e}")
            sys.exit(1)

        try:
            vocab_path = self.model.get_path_to_vocab_file()
            with open(vocab_path, 'r', encoding='utf-8') as f:
                self.token_to_id = json.load(f)

            self.id_to_token = {
                int(v): k for k, v in self.token_to_id.items()}
            print(f"\nVocabulary loaded! ({len(self.id_to_token)} tokens)",
                  file=sys.stderr)
        except Exception as e:
            print(f"Error occurred: {e}")
            sys.exit(1)

    def text_to_token_ids_list(self, text: str) -> list[int] | Any:
        """Convert text to a list of token IDs."""
        return self.model.encode(text).tolist()[0]

    def token_id_to_string(self, token_id: int) -> str | Any:
        """Convert a single token ID back to its string representation."""
        raw_string = self.id_to_token.get(token_id, "")
        return raw_string.replace("Ġ", " ")

    def get_logits_list(self, input_ids: list[int]) -> list[float] | Any:
        """Get the raw probabilities for the next token."""
        return self.model.get_logits_from_input_ids(input_ids)
