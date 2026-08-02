import argparse
import json
import sys
import os
from src.llm_manager import LLMManager
from src.decoder import generate_constrained_decod
from src.schema import FunctionCall, FunctionDef


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
            func_data = json.load(f)
        functions_def: list[FunctionDef] = [
            FunctionDef(**func) for func in func_data]
        with open(args.input, 'r') as f:
            prompts_data = json.load(f)
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

    llm = LLMManager()
    results = []

    for item in prompts_data:
        prompt_text = item["prompt"]
        print(f"\n processing {prompt_text}")

        raw_output = generate_constrained_decod(
            prompt=prompt_text, llm=llm, func=functions_def, max_tokens=50)

        try:
            parsed_json = json.loads(raw_output)

            validate_pydantic = FunctionCall(
                prompt=prompt_text,
                name=parsed_json.get("name", ""),
                parameters=parsed_json.get("parameters", {})
            )

            results.append(validate_pydantic.model_dump())
        except Exception as e:
            print(f"Error occurred when parsing output: {e}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
