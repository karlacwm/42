import json
import os
from typing import Any
from src.visualizer import Visualizer


class FileHandler:
    """Handles all reading and writing of files with error recovery."""

    def load_json(self, filepath: str) -> list[Any] | dict[str, Any]:
        """
        Attempts to load a JSON file.
        If the file is missing or corrupted, it catches the error safely.
        """
        if not os.path.exists(filepath):
            print(f"Error caught: '{filepath}' does not exist.")
            # Error Recovery: Return an empty list so the program doesn't crash
            return []

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data: list[Any] | dict[str, Any] = json.load(file)
                return data

        except json.JSONDecodeError as e:
            print(f"Error caught: '{filepath}' contains invalid JSON - {e}")
            # Error Recovery: Return empty list to gracefully skip
            return []

        except Exception as e:
            print(
                f"Error occurred: failed to read '{filepath}' - {e}")
            return []

    def save_json(self, filepath: str, data: list[Any]) -> None:
        """
        Safely saves data to a JSON file,
        creating the output folder if it doesn't exist.
        """
        try:
            # Ensure the output directory exists (e.g., data/output/)
            directory = os.path.dirname(filepath)
            if directory:
                os.makedirs(directory, exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
            Visualizer.print_done(filepath)

        except Exception as e:
            print(f"Error occurred saving output to '{filepath}': {e}")
