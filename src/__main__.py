import argparse
import json
import sys

from src.llm_manager import LLMManager
from src.decoder import generate_constrained_deco
from src.schema import FunctionDef


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Function Calling tool")
    parser.add_argument("--functions_definition", type=str,
                        default="data/input/functions_definition.json")
    parser.add_argument("--input", type=str,
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output", type=str,
                        default="data/output/function_calling_results.json")
    args = parser.parse_args()

    try:
        with open(args.functions_definition, 'r') as f:
            prompts_data = json.load(f)
        functions_def: list[FunctionDef] = [
            FunctionDef(**fn) for fn in prompts_data]

        with open(args.input, 'r') as f:
            prompts_data = json.load(f)
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

    llm = LLMManager()
    first_prompt = prompts_data[0]["prompt"]
    final_output = generate_constrained_deco(
        prompt=first_prompt, llm=llm, func=functions_def, max_tokens=50)

    print(f"\nFinal Unconstrained Output:\n{first_prompt} {final_output}")


if __name__ == "__main__":
    main()
