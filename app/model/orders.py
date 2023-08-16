from _decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class State(Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELED = "CANCELED"


class OrderInput(BaseModel):
    stoks: str
    quantity: int


class OrderOutput(BaseModel):
    input_id: str
    stoks: str
    quantity: float
    status: str


class OrderId(BaseModel):
    input_id: str


class Error(BaseModel):
    code: int
    message: str
