from Config_Logger.logger import logging
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError
from typing import List


class Request(BaseModel):
    input: str

    @field_validator('input', mode='before')  # In pydantic 1: pre=True
    def value_must_be_a_str(cls, v):
        if type(v) != str:
            error_msg = f"input '{v}' is not a valid string."
            logging.error(f"Request: {v}")
            logging.error(f"422 {error_msg}")
            raise PydanticCustomError(
                str(type(v)),
                error_msg,
                dict(wrong_value=v)
            )
        return v


class Response(BaseModel):
    output: List[str]
