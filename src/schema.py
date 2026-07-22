# {
#   "name": "fn_add_numbers",
#   "description": "Add two numbers together and return their sum.",
#   "parameters": {
#     "a": {"type": "number"},
#     "b": {"type": "number"}
#   },
#   "returns": {"type": "number"}
# }

from pydantic import BaseModel
from typing import Any

# 1. Define what a single Parameter looks like


class ParameterDef(BaseModel):
    type: str

# 2. Define what the Return block looks like


class ReturnDef(BaseModel):
    type: str

# 3. Define the main Function Definition


class FunctionDef(BaseModel):
    name: str
    description: str
    # Parameters is a dictionary where the key is the argument name (like "a")
    # and the value is the ParameterDef (like {"type": "number"})
    parameters: dict[str, ParameterDef]
    returns: ReturnDef


class FunctionCall(BaseModel):
    name: str
    # Arguments can be numbers, strings, etc., so we use Dict[str, Any]
    arguments: dict[str, Any]
