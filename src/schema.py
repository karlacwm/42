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
