from pydantic import BaseModel
from typing import Any


class ParameterDef(BaseModel):
    type: str


class ReturnDef(BaseModel):
    type: str


class FunctionDef(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParameterDef]
    returns: ReturnDef


class Output(BaseModel):
    prompt: str
    name: str
    parameters: dict[str, Any]


# example output -- save to data/output/function_calling_results.json
# [
#   {
#       "prompt": "What is the sum of 2 and 3?",
#       "name": "fn_add_numbers",
#       "parameters": {"a": 2.0, "b": 3.0}
#   },
#   {
#       "prompt": "Reverse the string 'hello'",
#       "name": "fn_reverse_string",
#       "parameters": {"s": "hello"}
#   }
# ]
