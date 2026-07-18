from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int
    message: str
    response: Optional[T] = None
