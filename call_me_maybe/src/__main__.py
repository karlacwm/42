import argparse
import sys


def main() -> None:
    from src.workflow import Workflow
    try:
        parser = argparse.ArgumentParser(
            description="LLM Function Calling tool")
        parser.add_argument(
            "--functions_definition", type=str,
            default="data/input/functions_definition.json"
        )
        parser.add_argument(
            "--input", type=str,
            default="data/input/function_calling_tests.json"
        )
        parser.add_argument(
            "--output", type=str,
            default="data/output/function_calling_results.json"
        )

        args = parser.parse_args()

        callme = Workflow()
        callme.run(
            functions_path=args.functions_definition,
            input_path=args.input,
            output_path=args.output
        )
    except Exception as e:
        print(f"Error occured: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nYou ended the call.")
        sys.exit(1)
