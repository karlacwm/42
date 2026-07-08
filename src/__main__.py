import argparse
import json
import sys

# NEW: Import the LLM SDK provided by the project
from llm_sdk import Small_LLM_Model


def main() -> None:
    # --- PHASE 1: PARSING AND LOADING (Same as before) ---
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
            functions_def = json.load(f)
        with open(args.input, 'r') as f:
            prompts_data = json.load(f)
    except Exception as e:
        print(f"Error loading files: {e}")
        sys.exit(1)

    print("✅ Phase 1: Files loaded successfully!")

    # --- PHASE 2: CONNECTING THE LLM ---
    print("\n--- Starting Phase 2: LLM Connection ---")

    # 1. Initialize the model
    print("Initializing Small_LLM_Model (This might take a few seconds)...")
    try:
        llm = Small_LLM_Model()
        print("✅ Model initialized!")
    except Exception as e:
        print(f"❌ Failed to initialize model: {e}")
        sys.exit(1)

    # 2. Load the Vocabulary
    try:
        # UPDATED: Use the correct method name found in the SDK source code
        vocab_path = llm.get_path_to_vocab_file()
        with open(vocab_path, 'r', encoding='utf-8') as f:
            token_to_id = json.load(f)

        # REVERSAL: The JSON maps {"word": 123}, but we want {123: "word"} for easy lookup later!
        id_to_token = {int(v): k for k, v in token_to_id.items()}
        print(f"✅ Vocabulary loaded! (Found {len(id_to_token)} tokens)")
    except Exception as e:
        print(f"❌ Failed to load vocabulary: {e}")
        sys.exit(1)

    # 3. Test Tokenization
    first_prompt = prompts_data[0]["prompt"]
    print(f"\nOriginal Prompt: '{first_prompt}'")

    # UPDATED: encode() returns a 2D tensor, so we convert it to a flat Python list
    input_ids_tensor = llm.encode(first_prompt)
    input_ids = input_ids_tensor.tolist()[0]
    print(f"Encoded Token IDs: {input_ids}")

    # Map those IDs back to text using our reversed dictionary
    mapped_text = [id_to_token.get(tok_id, "<UNKNOWN>")
                   for tok_id in input_ids]
    print(f"Tokens mapped back to text: {mapped_text}")

    print("\n✅ Phase 2 Complete!")


if __name__ == "__main__":
    main()
