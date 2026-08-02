import numpy as np
from src.llm_manager import LLMManager
from src.schema import FunctionDef


class FunctionPicking:
    """Handles Stage 1: Asking the AI which function to use."""

    def __init__(self, llm: LLMManager) -> None:
        # We pass the LLM engine into the selector so it can use it
        self.llm = llm

    def select_function(self, prompt: str, functions: list[FunctionDef]
                        ) -> str:
        """
        Builds a menu of functions, asks the AI which one fits the prompt,
        and returns the matched function name.
        """
        valid_names = [f.name for f in functions]

        # Build a simple menu so the AI knows what the functions actually do!
        menu = ""
        for f in functions:
            menu += f"- {f.name}: {f.description}\n"

        stage1_prompt = (
            f"Question: {prompt}\n"
            f"Here are the available functions and what they do:\n{menu}\n"
            "Based on the question, which function should be used?"
            "Answer with EXACTLY one function name:"
        )

        input_ids = self.llm.text_to_token_ids_list(stage1_prompt)
        generated_name = ""
        matched_name = None

        # Give the AI 20 steps to type the name
        for _ in range(20):
            logits = np.array(self.llm.get_logits_list(input_ids))
            best_token = int(np.argmax(logits))
            input_ids.append(best_token)

            piece = self.llm.token_id_to_string(best_token)
            generated_name += piece

            # Check if it typed a valid function name yet
            for name in valid_names:
                if name in generated_name:
                    matched_name = name
                    break

            if matched_name:
                break

        # Fallback: Safely default to first func if AI gets completely lost
        if not matched_name:
            matched_name = valid_names[0]

        return matched_name
