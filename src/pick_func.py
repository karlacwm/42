import numpy as np
import re
from src.llm_manager import LLMManager
from src.schema import FunctionDef


class FunctionPicking:
    """Handles Stage 1: Asking the AI which function to use."""

    @staticmethod
    def _extract_keywords(text: str) -> set[str]:
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        stopwords = {
            "a", "an", "and", "be", "do", "for", "from", "how", "i",
            "in", "is", "it", "of", "on", "or", "the", "to", "use",
            "what", "when", "where", "which", "who", "why", "with",
        }
        return {token for token in tokens if token not in stopwords}

    def _best_keyword_score(
            self, prompt: str, functions: list[FunctionDef]) -> int:
        prompt_keywords = self._extract_keywords(prompt)
        best_score = 0

        for function in functions:
            function_keywords = self._extract_keywords(
                f"{function.name} {function.description}")
            score = len(prompt_keywords & function_keywords)
            if score > best_score:
                best_score = score

        return best_score

    def __init__(self, llm: LLMManager) -> None:
        self.llm = llm

    def select_function(self, prompt: str, functions: list[FunctionDef]
                        ) -> str:
        """
        Builds a menu of functions, asks the AI which one fits the prompt,
        and returns the matched function name.
        """
        valid_names = [f.name for f in functions]
        valid_names_with_unknown = valid_names + ["Unknown"]

        if self._best_keyword_score(prompt, functions) == 0:
            return "Unknown"

        menu = ""
        for f in functions:
            menu += f"- {f.name}: {f.description}\n"

        menu += ("- Unknown: If none of the above functions fit the question, "
                 "choose this option.")

        stage1_prompt = (
            f"Question: {prompt}\n"
            f"Here are the available functions and what they do:\n{menu}\n"
            "Based on the question, which function should be used?\n"
            "If all options are bad, choose 'Unknown'.\n"
            "Answer with EXACTLY one function name:"
        )

        input_ids = self.llm.text_to_token_ids_list(stage1_prompt)
        generated_name = ""
        matched_name = None

        for _ in range(20):
            logits = np.array(self.llm.get_logits_list(input_ids))
            best_token = int(np.argmax(logits))
            input_ids.append(best_token)

            piece = self.llm.token_id_to_string(best_token)
            generated_name += piece

            for name in valid_names_with_unknown:
                if name in generated_name:
                    matched_name = name
                    break

            if matched_name:
                break

        if not matched_name:
            matched_name = "Unknown"

        return matched_name
