from pydantic import BaseModel
from typing import List

class Request(BaseModel):
    input: str

class Response(BaseModel):
    output: List[str]
