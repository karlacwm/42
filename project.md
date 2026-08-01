Chapter IV
IV.1 General Rules
• Your project must be written in Python 3.10 or later.
• Your project must adhere to the flake8 coding standard.
• Your functions should handle exceptions gracefully to avoid crashes. Use try-except
blocks to manage potential errors. Prefer context managers for resources like files or
connections to ensure automatic cleanup. If your program crashes due to unhandled
exceptions during the review, it will be considered non-functional.
• All resources (e.g., file handles, network connections) must be properly managed to
prevent leaks. Use context managers where possible for automatic handling.
• Your code must include type hints for function parameters, return types, and variables where applicable (using the typing module). Use mypy for static type checking. All functions must pass mypy without errors.
• Include docstrings in functions and classes following PEP 257 (e.g., Google or
NumPy style) to document purpose, parameters, and returns.

IV.2 Makefile
Include a Makefile in your project to automate common tasks. It must contain the
following rules (mandatory lint implies the specified flags; it is strongly recommended to
try –strict for enhanced checking):
• install: Install project dependencies using pip, uv, pipx, or any other package
manager of your choice.
• run: Execute the main script of your project (e.g., via Python interpreter).
• debug: Run the main script in debug mode using Python’s built-in debugger (e.g.,
pdb).
• clean: Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to
keep the project environment clean.
• lint: Execute the commands flake8 . and mypy . --warn-return-any
--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
--check-untyped-defs
• lint-strict (optional): Execute the commands flake8 . and mypy . --strict

IV.3 Additional Requirements
• All classes must use pydantic for validation.
• You can use the numpy and json packages.
• The use of dspy (or any similar package) is completely forbidden including pytorch,
huggingface package, transformers, outlines, etc.
• You need to use the following models:
◦ Qwen/Qwen3-0.6B (default)
◦ You can use other models as long as your project works with Qwen/Qwen3-
0.6B.
• The function to call should be chosen using the LLM, not with heuristics or any
other sort of medieval magic.
• It is forbidden to use any private methods or attributes from the llm_sdk package.
• You should create a virtual environment and install the packages numpy and
pydantic using uv. To use llm_sdk, you can copy it in the same directory as the
one src is in.
• The reviewer, as well as the moulinette, will just run uv sync.
• All errors should be handled gracefully. Your program must never crash unexpectedly and must always provide clear error messages to the user.

IV.4 Usage
Your program must be run using the following command (where src is the folder containing your files):
Running the program
uv run python -m src [--functions_definition <function_definition_file>] [--input <input_file>] [--output <output_file>]

By default, the program will read input files from the data/input/
directory and write output to the data/output/ directory. You
can optionally specify custom paths using the --input and --output
arguments. For example:
uv run python -m src
--functions_definition data/input/functions_definition.json
--input data/input/function_calling_tests.json
--output data/output/function_calls.json

Chapter V
V.1 Summary
In this project, you will create a function calling tool that translates natural language
prompts into structured function calls. Given a question like "What is the sum of 40 and
2?", your solution should not return 42, but instead provide:
• The function name: fn_add_numbers
• The arguments: {"a": 40, "b": 2}
Your implementation must use constrained decoding to guarantee 100% valid JSON
output, ensuring near-perfect reliability even with a small 0.5B parameter model.

V.2 Input Files
Your solution will process two input files located in the data/input/ directory:
• function_calling_tests.json: contains a JSON array of natural language prompts
that your system must process.
• function_definitions.json: contains the available functions your system can
call. Each function includes:
◦ Function name
◦ Argument names and types
◦ Return type
◦ Description

V.3 LLM Interaction

V.3.1 The LLM SDK
Attached to this project, you’ll find a wrapper class Small_LLM_Model in the llm_sdk
package that you can use to interact with the LLM.
The SDK provides several essential methods:
• get_logits_from_input_ids(input_ids: Tensor) -> Tensor
Takes an input_ids tensor and returns the raw logits after calling the LLM model.
• get_path_to_vocabulary_json() -> str
Returns the path to a JSON file containing the structured correspondence between
input_ids and tokens.
• encode(text: str) -> List[int]
Encodes a text string into its corresponding list of token IDs using the model’s
tokenizer.
• decode(token_ids: List[int]) -> str (optional)
Optionally decodes a list of token IDs back into a text string.

V.3.2 The Generation Pipeline
The LLM generation process follows these steps:
1. Prompt: Your natural language question
Example: "What is the sum of 2 and 3?"
2. Tokenization: The text is broken into subword units (tokens). Unlike simple word
splitting, tokenizers often include leading spaces, handle punctuation, and split
words into smaller components using algorithms such as BPE or SentencePiece.
Example (realistic): ["What", "Gis ˙ ", "Gthe ˙ ", "Gsum ˙ ", "Gof ˙ ", "G2˙ ", "Gand ˙ ", "G3˙ ", "?"]
Note: The symbol "˙G", indicates a preceding space; real tokenizers preserve such
details to reconstruct text accurately.
3. Input IDs: Tokens are converted to numerical IDs the model understands.
Example (illustrative): [892, 318, 262, 4771, 286, 16, 290, 17, 30]
4. LLM Processing: The model processes these numbers through its neural network.
5. Logits: The model outputs probability scores for each possible next token.
Example: token_5: 0.001, token_42: 0.85, token_100: 0.02, ...
6. Token Selection: The next token is chosen based on these probabilities, usually
the one with the highest score.
At this stage, techniques like constrained decoding can be applied to restrict the
token choices and ensure outputs follow a specific structure, such as generating
100% valid JSON.
Important: This process repeats token-by-token. Each generated token is added to the
prompt, and steps 2-6 repeat until the complete response is generated.
Simplified view:
Prompt -> Tokenization -> Input IDs -> LLM -> Logits -> Next Token Selection

V.3.3 Understanding Constrained Decoding
Language models generate text one token at a time. At each step, the model produces
a probability distribution (logits) over all possible next tokens. Normally, you would
sample from this distribution or pick the highest probability token.
Constrained decoding intervenes in this process by modifying the logits before token
selection:
1. The model produces logits for all possible tokens.
2. You identify which tokens would maintain both a valid JSON structure and compliance with the expected schema.
3. You set logits for invalid tokens (those breaking the schema or structure) to negative
infinity.
4. You sample only from the remaining valid tokens.
In this project, constrained decoding must not only ensure syntactically valid JSON
but also enforce a specific schema. For instance, if the JSON field "firmware" can
only take a few predefined values, the decoder should restrict token selection to those
allowed options. This guarantees that every generated token maintains both structural
and semantic validity, enforcing the required schema. As a result, the produced JSON is
100% retrievable and can always be parsed without errors.
Your solution must NOT rely on the model spontaneously producing
correct JSON from a prompt. Prompting the model with function
definitions and hoping for structured output is not reliable, and
it is not the skill we expect you to develop here.
Think about how you can use the vocabulary JSON file to map between
tokens and their string representations. This is crucial for
determining which tokens are valid at each generation step.

V.4 Output File Format
Your program will produce a single JSON file: data/output/function_calling_results.json.
For each prompt, add a JSON object to this file. Each object in the array must contain
exactly the following keys:
• prompt (string): The original natural-language request
• name (string): The name of the function to call
• parameters (object): All required arguments with the correct types

V.4.1 Example Output
[
    {
        "prompt": "What is the sum of 2 and 3?",
        "name": "fn_add_numbers",
        "parameters": {"a": 2.0, "b": 3.0}
    },
    {
        "prompt": "Reverse the string 'hello'",
        "name": "fn_reverse_string",
        "parameters": {"s": "hello"}
    }
]

V.4.2 Validation Rules
• The file must be valid JSON (no trailing commas, no comments)
• Keys and types must match the schema in function_definitions.json exactly
• No extra keys or prose are allowed anywhere in the output
• All required arguments must be present
• Argument types must match the function definition (number, string, boolean, etc.)

V.5 Performance and Reliability
Your implementation should achieve:
• Near-perfect accuracy: 90%+ correct function selection and argument extraction
• 100% valid JSON: Every output must be parseable and schema-compliant
• Reasonable speed: Process all test prompts in under 5 minutes on standard
hardware
• Robust error handling: Gracefully handle malformed inputs, missing files, and
edge cases

V.6 Testing Your Implementation
To verify your solution works correctly:
1. Ensure input files are in the data/input/ directory
2. Run: uv run python -m src [–functions_definition <function_definition_file>]
[–input <input_file>] [–output <output_file>]
3. Check that output/function_calling_results.json is created
4. Validate the JSON structure and content
5. Verify function names and argument types match the definitions
Test with various edge cases: empty strings, large numbers, special
characters, wrong types, ambiguous prompts, and functions with
multiple parameters.

V.7 Readme Requirements

V.8 Bonus
Optional, one point for one feature, five points maximum
• Support for multiple LLM models beyond Qwen/Qwen3-0.6B
• Advanced error recovery mechanisms
• Performance optimizations (caching, batching)
• Comprehensive test suite
• Visualization of the generation process
• Support for complex nested function arguments
• Public implementation of tokenizer encode and optional decode methods
• Demonstration of how encoding and decoding integrate with constrained decoding
