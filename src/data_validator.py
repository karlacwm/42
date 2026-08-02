from pydantic import ValidationError
from src.schema import FunctionDef, FunctionCall


class DataValidator:
    """Validates raw input and output dictionaries using Pydantic models."""

    @staticmethod
    def validate_function_definitions(
            raw_defs: list[dict]) -> list[FunctionDef]:
        """Ensures input function definitions match our Pydantic schema."""
        valid_defs = []
        for index, raw_item in enumerate(raw_defs):
            try:
                # Pydantic validates the structure automatically
                func_obj = FunctionDef(**raw_item)
                valid_defs.append(func_obj)
            except ValidationError as err:
                print(f"Validation Error: function def #{index} - {err}")
        return valid_defs

    @staticmethod
    def validate_output_call(prompt: str, name: str,
                             params: dict) -> dict | None:
        """Ensures the generated result matches the required output schema."""
        try:
            call_obj = FunctionCall(prompt=prompt, name=name,
                                    parameters=params)
            return call_obj.model_dump()
        except ValidationError as err:
            print(f"Validation Error: output schema - {err}")
            return None
