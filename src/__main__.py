import argparse
import json
import sys


def main() -> None:
    # 1. Set up argument parsing to accept the paths
    parser = argparse.ArgumentParser(description="LLM Function Calling tool")

    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to the functions definition file"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to the input test prompts file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path to the output file"
    )

    # Parse the arguments provided by the user (or use defaults)
    args = parser.parse_args()

    # 2. Load the JSON files safely
    try:
        # Load the function definitions (the rules)
        with open(args.functions_definition, 'r') as f:
            functions_def = json.load(f)

        # Load the test prompts (the questions)
        with open(args.input, 'r') as f:
            prompts_data = json.load(f)

    except FileNotFoundError as e:
        print(f"Error: Could not find required input file. {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: An input file contains invalid JSON. {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    # 3. Print a quick test to verify everything is working (we will remove this later)
    print("✅ Phase 1 Complete: Successfully loaded files!")
    print(f"Number of available functions: {len(functions_def)}")
    print(f"Number of test prompts: {len(prompts_data)}\n")

    print("--- First function definition ---")
    print(json.dumps(functions_def[0], indent=2))

    print("\n--- First prompt ---")
    print(json.dumps(prompts_data[0], indent=2))


if __name__ == "__main__":
    main()
