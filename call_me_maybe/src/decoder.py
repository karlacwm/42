import json
import numpy as np
from src.llm_manager import LLMManager
from src.schema import FunctionDef


class Decoder:
    """Generating the JSON parameters for a chosen function."""

    def __init__(self, llm: LLMManager) -> None:
        self.llm = llm

    def generate_parameters(
            self, prompt: str, matched_name: str,
            functions: list[FunctionDef], max_tokens: int = 150) -> str:
        """
        Asks the AI to generate JSON parameters for the selected function
        and visualizes the output token-by-token.
        """
        if matched_name == "Unknown":
            return json.dumps({"name": matched_name, "parameters": {}})

        expected_params = []
        matched_desc = ""

        for f in functions:
            if f.name == matched_name:
                expected_params = list(f.parameters.keys())
                matched_desc = f.description
                break

        stage2_prompt = (
            f"Question: {prompt}\n"
            f"Function: '{matched_name}' ({matched_desc})\n"
            "If function is 'Unknown', return an empty parameters.\n"
            "Hint: Replace all numbers in a string, \
            the regex code is exactly \\d+. \
            Replace a word in a string, means regex is the word. \
            Replace all vowels in a string, \
            means the regex code is a|e|i|o|u."
            "\nOutput ONLY a valid JSON dictionary containing the parameters "
            f"{expected_params}. Extract the correct values from the Question."
            "\nJSON:"
        )

        input_ids = self.llm.text_to_token_ids_list(stage2_prompt)
        generated_params = ""

        try:
            brace_seq = self.llm.text_to_token_ids_list("{")
            brace_seq_list = list(brace_seq) if not isinstance(
                brace_seq, list) else brace_seq
            required_first_brace = brace_seq_list[0] if (
                brace_seq_list) else None
        except Exception:
            required_first_brace = None

        for step in range(max_tokens):
            logits = np.array(self.llm.get_logits_list(input_ids))

            if step == 0 and required_first_brace is not None:
                masked = np.full_like(logits, -1e9)
                if 0 <= required_first_brace < len(masked):
                    masked[required_first_brace] = logits[required_first_brace]
                    best_token = int(np.argmax(masked))
                else:
                    best_token = int(np.argmax(logits))
            else:
                best_token = int(np.argmax(logits))

            input_ids.append(best_token)

            piece = self.llm.token_id_to_string(best_token)
            generated_params += piece

            open_brackets = generated_params.count('{')
            close_brackets = generated_params.count('}')
            if open_brackets > 0 and open_brackets == close_brackets:
                break

        print()

        start_idx = generated_params.find('{')
        end_idx = generated_params.rfind('}') + 1

        if start_idx != -1 and end_idx != -1:
            clean_params = generated_params[start_idx:end_idx]
        else:
            clean_params = "{}"

        clean_params = self._repair_json_escapes(clean_params)

        try:
            parameters = json.loads(clean_params)
        except json.JSONDecodeError:
            parameters = {}

        return json.dumps({"name": matched_name, "parameters": parameters})

    @staticmethod
    def _repair_json_escapes(json_text: str) -> str:
        """Escape stray backslashes so text remain valid JSON."""
        repaired = []
        index = 0

        while index < len(json_text):
            character = json_text[index]
            if character == "\\" and index + 1 < len(json_text):
                next_character = json_text[index + 1]
                if next_character not in '"\\/bfnrtu':
                    repaired.append("\\\\")
                    index += 1
                    continue

            repaired.append(character)
            index += 1

        return "".join(repaired)
