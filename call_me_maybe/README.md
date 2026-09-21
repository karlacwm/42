*This project has been created as part of the 42 curriculum by wcheung.*

## Description

This project implements a function calling pipeline designed to map prompts into strictly formatted JSON function calls. The system is designed for small LLM (like Qwen 0.6B), without relying on massive compute resources or external parsing APIs.

The system follows a two-stage constrained decoding approach: function selection (stage 1) and parameter generation (stage 2). Stage 1 chooses a function from the available definitions, while stage 2 extracts the arguments and formats them as JSON. It focuses on schema validation and an output formatted in the expected structure.

## Instruction
First step:

```
make install
```

Usage:

```
uv run python -m src [--functions_definition <function_definition_file>] [--input <input_file>] [-- output <output_file>]
```

Test it with:

(to solve storage porblem we redirect the hugging face cache to HF_HOME=/goinfre/$USER/hf_cache)

```
HF_HOME=/goinfre/$USER/hf_cache uv run python -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calls.json
```

but you can also just run it with:

```
make run
```

Moulinette:

```
cd moulinette && uv sync
uv run python -m moulinette prepare_exercises
uv run python -m moulinette grade_student_answers ../data/output/function_calling_results.json
```

Test flake8 and mypy:
```
make lint 
make lint-strict
```

## Additionals
### Algorithm explanation

I implemented a two-stage pipeline to convert prompts into structured function calls in JSON format.

Stage 1
- is about selecting the matching function from the provided function definitions.
Instead of going to the LLM directly, there is a keyword check if there is an overlap with available function names or descriptions. If not, it will simply return "Unkown" before asking the LLM. 

Stage 2
- is about when a function is selected, the output will be generated in JSON format, with the necessary elements (prompt, name and parameters)

Pydantic is used for data type validation.

### Design decisions

Constrained decoding
- small LLM models often produce malformed JSON
- splitting function choice and parameter extraction reduces complexity per step

"Unknown" function
- for ambiguous prompts or prompts that cannot be matched, they should not be forced into a wrong function
- "unknown" function plus empty parameters is added in the function selection process to make the output more reliable

### Challenges faced

Challenge 1: storage
- "not enough space" to install dependencies
- fix: git clone repo in goinfre and export uv and huggingface cache into another directory in goinfre 

Challenge 2: wrong function selection
- wrong function selection despite separating function selection and output formatting
- also wrong function selected when the prompt asked for something totally irrelevant
- fix: more descriptive prompt at stage 1 and added an unkown function if no function provided can match the prompt

Challenge 3: bad input files
- empty strings in prompts, invalid JSON format, missing input files (function def and prompts) etc
- fix: added more checks on parsing the input and error handling so the program doesnt crash

## Resources

LLM
[[1]](https://seantrott.substack.com/p/tokenization-in-large-language-models)
[[2]](https://medium.com/thedeephub/all-you-need-to-know-about-tokenization-in-llms-7a801302cf54)
[[3]](https://www.understandingai.org/p/large-language-models-explained-with)
[[4]](https://jillanisofttech.medium.com/understanding-the-differences-between-encoders-decoders-and-encoder-decoder-llms-a-mentor-mentee-58bb73a0a0ac)
[[5]](https://magazine.sebastianraschka.com/p/understanding-encoder-and-decoder)


JSON
[[1]](https://www.geeksforgeeks.org/python/json-load-in-python/)

Python
[[1]](https://mimo.org/glossary/python/argparse)
[[2]](https://www.geeksforgeeks.org/python/python-os-makedirs-method/)

Pydantic
[[1]](https://pydantic.dev/docs/validation/dev/concepts/serialization/)

Visualizer
[[1]](https://emojicombos.com/kaomoji)
[[2]](https://www.geeksforgeeks.org/python/clear-screen-python/)
[[3]](https://www.geeksforgeeks.org/python/python-subprocess-module/)


## AI usage
AI is used for:
- understanding the subject and tasks
- project planning and guidance
- explaining me LLMs, tokenisation, encoding, decoding, constrained decoding
- answering my questions when I did not understand the above-mentioned concepts
- debugging and pointing out my problems
- advising on improvements and what I missed out