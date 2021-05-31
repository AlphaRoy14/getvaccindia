from pydantic import BaseModel
from typing import Optional, Any


class ResponseModel(BaseModel):
    message: str = "Success"
    error: Optional[str] = None
    data: Optional[Any] = None
