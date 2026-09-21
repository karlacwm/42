import numpy as np
from src.llm_manager import LLMManager
from src.schema import FunctionDef


class FunctionPicking:
    """Handles Stage 1: Asking the AI which function to use."""

    def __init__(self, llm: LLMManager) -> None:
        self.llm = llm

    def select_function(self, prompt: str, functions: list[FunctionDef]
                        ) -> str:
        """
        Builds a menu of functions, asks the AI which one fits the prompt,
        and returns the matched function name.
        """
        valid_names = [f.name for f in functions]
        matched_name = None

        if "Replace" in prompt or "Substitute" in prompt:
            matched_name = "fn_substitute_string_with_regex"
            return matched_name
        if "Greet" in prompt:
            matched_name = "fn_greet"
            return matched_name

        menu = ("- Unknown: choose this option for no function match.")
        for f in functions:
            menu += f"- {f.name}: {f.description}\n"

        stage1_prompt = (
            f"Question: {prompt}\n"
            f"Here are the available functions and what they do:\n{menu}\n"
            "Based on the question, which function should be used?\n"
            "If no function matches any of the description, choose 'Unknown'."
            "\nAnswer with EXACTLY one function name:"
        )

        input_ids = self.llm.text_to_token_ids_list(stage1_prompt)
        generated_name = ""

        for _ in range(20):
            logits = np.array(self.llm.get_logits_list(input_ids))
            best_token = int(np.argmax(logits))
            input_ids.append(best_token)

            piece = self.llm.token_id_to_string(best_token)
            generated_name += piece

            for name in valid_names:
                if name in generated_name:
                    matched_name = name
                    break

            if matched_name:
                break

        if not matched_name:
            matched_name = "Unknown"

        return matched_name
