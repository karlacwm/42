import argparse
import json
import sys

# Import our new modularized code
from src.llm_manager import LLMManager
from src.decoder import generate_unconstrained


def main() -> None:
    # 1. Parse Arguments
    parser = argparse.ArgumentParser(description="LLM Function Calling tool")
    parser.add_argument("--functions_definition", type=str,
                        default="data/input/functions_definition.json")
    parser.add_argument("--input", type=str,
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output", type=str,
                        default="data/output/function_calling_results.json")
    args = parser.parse_args()

    # 2. Load Files
    try:
        with open(args.functions_definition, 'r') as f:
            functions_def = json.load(f)
        with open(args.input, 'r') as f:
            prompts_data = json.load(f)
    except Exception as e:
        print(f"Error loading files: {e}")
        sys.exit(1)

    print("Files loaded successfully!")

    # 3. Initialize LLM Manager
    llm = LLMManager()

    # 4. Run the Decoder Experiment
    first_prompt = prompts_data[0]["prompt"]

    final_output = generate_unconstrained(
        prompt=first_prompt, llm=llm, max_tokens=20)

    print(f"\nFinal Unconstrained Output:\n{first_prompt} {final_output}")
    print("\nRefactoring Complete!")


if __name__ == "__main__":
    main()
