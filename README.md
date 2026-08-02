*This project has been created as part of the 42 curriculum by wcheung.*

## Description



## Instruction

uv run python -m src [--functions_definition <function_definition_file>] [--input <input_file>] [--
output <output_file>]

uv run python -m src
--functions_definition data/input/functions_definition.json
--input data/input/function_calling_tests.json
--output data/output/function_calls.json

uv sync
uv run python -m moulinette prepare_exercises
uv run python -m moulinette grade_student_answers ../data/output/function_calling_results.json



## Additionals
### Algorithm explanation
Describe your constrained decoding approach in detail
### Design decisions
Explain key choices in your implementation
### Performance analysis
Discuss accuracy, speed, and reliability of your solution
### Challenges faced
Document difficulties encountered and how you solved them
### Testing strategy
Describe how you validated your implementation
### Example usage
Provide clear examples of running your program

## Resources

LLM
https://seantrott.substack.com/p/tokenization-in-large-language-models
https://medium.com/thedeephub/all-you-need-to-know-about-tokenization-in-llms-7a801302cf54
https://www.understandingai.org/p/large-language-models-explained-with
https://jillanisofttech.medium.com/understanding-the-differences-between-encoders-decoders-and-encoder-decoder-llms-a-mentor-mentee-58bb73a0a0ac
https://magazine.sebastianraschka.com/p/understanding-encoder-and-decoder


JSON
https://www.geeksforgeeks.org/python/json-load-in-python/

Python
https://www.geeksforgeeks.org/python/python-os-makedirs-method/

Pydantic
https://pydantic.dev/docs/validation/dev/concepts/serialization/

Visualizer
https://emojicombos.com/kaomoji
https://www.geeksforgeeks.org/python/clear-screen-python/
https://www.geeksforgeeks.org/python/python-subprocess-module/