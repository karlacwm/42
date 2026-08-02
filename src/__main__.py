import argparse
from src.workflow import Workflow


def main() -> None:
    # 1. Setup terminal arguments exactly as the rubric requires
    parser = argparse.ArgumentParser(description="LLM Function Calling tool")
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

    # 2. Create the manager and run the program!
    app = Workflow()
    app.run(
        functions_path=args.functions_definition,
        input_path=args.input,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
