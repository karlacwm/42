from typing import Any
from pydantic import ValidationError
from src.schema import FunctionDef, Output


class DataValidator:
    """Validates raw input and output dictionaries using Pydantic models."""

    @staticmethod
    def validate_function_definitions(
            raw_defs: list[dict[str, Any]]) -> list[FunctionDef]:
        """Ensures input function definitions match our Pydantic schema."""
        valid_defs = []
        for index, raw_item in enumerate(raw_defs):
            try:
                # Pydantic validates the structure automatically
                func_obj = FunctionDef(**raw_item)
                valid_defs.append(func_obj)
            except ValidationError as err:
                print(f"Validation error: function def #{index} - {err}")
        return valid_defs

    @staticmethod
    def validate_prompts(raw_prompts: list[dict[str, Any]]
                         ) -> list[dict[str, Any]]:
        """Ensures the input test file contains 'prompt' strings."""
        valid_prompts = []
        for index, item in enumerate(raw_prompts):
            if isinstance(item, dict) and "prompt" in item:
                valid_prompts.append(item)
            else:
                print(f"Validation error: #{index} - missing prompt key.")
        return valid_prompts

    @staticmethod
    def validate_output(prompt: str, name: str,
                        params: dict[str, Any]) -> dict[str, Any] | None:
        """Ensures the generated result matches the required output schema."""
        try:
            output_obj = Output(prompt=prompt, name=name,
                                parameters=params)
            return output_obj.model_dump()
        except ValidationError as err:
            print(f"Validation error: output schema - {err}")
            return None
