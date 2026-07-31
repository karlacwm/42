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


class FunctionCall(BaseModel):
    name: str
    arguments: dict[str, Any]

# {
#   "name": "fn_add_numbers",
#   "description": "Add two numbers together and return their sum.",
#   "parameters": {
#     "a": {"type": "number"},
#     "b": {"type": "number"}
#   },
#   "returns": {"type": "number"}
# }
