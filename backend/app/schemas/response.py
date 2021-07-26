from pydantic import BaseModel
from typing import Optional, Any
from schemas.subscriber import Subscriber


class ResponseModel(BaseModel):
    message: str = "Success"
    error: Optional[str] = None
    data: Optional[Any]


class SubscriberResponseModel(ResponseModel):
    data: Subscriber
