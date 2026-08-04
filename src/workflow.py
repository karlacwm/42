import json
import sys
from src.llm_manager import LLMManager
from src.handle_file import FileHandler
from src.validate_data import DataValidator
from src.pick_func import FunctionPicking
from src.decoder import Decoder
from src.visualizer import Visualizer


class Workflow:
    """The boss class that connects all the pieces of our program together."""

    def __init__(self) -> None:
        self.llm = LLMManager()

        self.file_handler = FileHandler()
        self.selector = FunctionPicking(self.llm)
        self.decoder = Decoder(self.llm)

    def run(self, functions_path: str, input_path: str,
            output_path: str) -> None:
        """Runs the entire process from loading files to saving the results."""

        raw_functions = self.file_handler.load_json(functions_path)
        raw_prompts = self.file_handler.load_json(input_path)

        functions = DataValidator.validate_function_definitions(
            raw_functions if isinstance(raw_functions, list) else []
        )
        prompts = DataValidator.validate_prompts(
            raw_prompts if isinstance(raw_prompts, list) else []
        )

        if not functions:
            print("Function data missing or invalid, cannot continue :(")
            return
        if not prompts:
            print("Prompts data missing or invalid, cannot continue :(")
            return

        final_results = []
        total_prompts = len(prompts)
        visualizer = Visualizer(total_prompts)
        Visualizer.print_start()

        for index, item in enumerate(prompts):
            prompt_text = item["prompt"]
            matched_name = self.selector.select_function(
                prompt_text, functions)

            raw_output = self.decoder.generate_parameters(
                prompt=prompt_text,
                matched_name=matched_name,
                functions=functions,
                max_tokens=150
            )

            try:
                parsed_json = json.loads(raw_output)
                func_name = parsed_json.get("name", "")
                params = parsed_json.get("parameters", {})

                for f in functions:
                    if f.name == func_name:
                        for key, val in params.items():
                            if (key in f.parameters and
                                    f.parameters[key].type == "number"):
                                try:
                                    params[key] = float(val)
                                except ValueError as e:
                                    print(f"ValueError occured: {e}.")
                        break

                validated_dict = DataValidator.validate_output(
                    prompt=prompt_text,
                    name=func_name,
                    params=params
                )

                if validated_dict:
                    final_results.append(validated_dict)

            except Exception as e:
                print(
                    f"Error occurred processing prompt #{index} "
                    f"({prompt_text}): {e}", file=sys.stderr)
            visualizer.update()
        visualizer.finish()
        self.file_handler.save_json(output_path, final_results)
