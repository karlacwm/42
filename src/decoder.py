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
        expected_params = []
        matched_desc = ""

        # Grab the exact parameter keys and description to guide the AI
        for f in functions:
            if f.name == matched_name:
                expected_params = list(f.parameters.keys())
                matched_desc = f.description
                break

        # The Stage 2 Prompt with our regex hint!
        stage2_prompt = (
            f"Question: {prompt}\n"
            f"Function: '{matched_name}' ({matched_desc})\n"
            "Output ONLY a valid JSON dictionary containing the parameters "
            f"{expected_params}. Extract the correct values from the Question."
            "\nJSON:"
        )

        input_ids = self.llm.text_to_token_ids_list(stage2_prompt)
        generated_params = ""

        print(f"\n[AI Typing Parameters for {matched_name}]: ", end="")

        # Generate tokens one by one
        for step in range(max_tokens):
            logits = np.array(self.llm.get_logits_list(input_ids))
            best_token = int(np.argmax(logits))
            input_ids.append(best_token)

            piece = self.llm.token_id_to_string(best_token)
            generated_params += piece

            # Stop when the JSON brackets are perfectly balanced
            open_brackets = generated_params.count('{')
            close_brackets = generated_params.count('}')
            if open_brackets > 0 and open_brackets == close_brackets:
                break

        print()

        # Chop off any extra hallucinated words and grab just the brackets
        start_idx = generated_params.find('{')
        end_idx = generated_params.rfind('}') + 1

        if start_idx != -1 and end_idx != -1:
            clean_params = generated_params[start_idx:end_idx]
        else:
            clean_params = "{}"

        # Assemble the perfect, crash-proof JSON string
        final_json_string = (f'{{"name": "{matched_name}", '
                             f'"parameters": {clean_params}}}')

        return final_json_string
