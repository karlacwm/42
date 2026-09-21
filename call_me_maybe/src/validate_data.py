import sys
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
                func_obj = FunctionDef(**raw_item)
                valid_defs.append(func_obj)
            except ValidationError as e:
                print(
                    f"\nValidation error: function def #{index} - {e}",
                    file=sys.stderr)
        return valid_defs

    @staticmethod
    def validate_prompts(raw_prompts: list[dict[str, Any]]
                         ) -> list[dict[str, Any]]:
        """Ensures the input test file contains usable prompt strings."""
        valid_prompts = []
        for index, item in enumerate(raw_prompts):
            if not isinstance(item, dict) or "prompt" not in item:
                print(f"\nValidation error: prompt #{index} "
                      "missing prompt key.", file=sys.stderr)
                continue

            prompt = item["prompt"]
            if not prompt.strip():
                print(
                    f"\nValidation error: prompt #{index} cannot be empty.",
                    file=sys.stderr)
                continue

            valid_prompts.append(item)
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
            print(
                f"\nValidation error: output schema - {err}", file=sys.stderr)
            return None
