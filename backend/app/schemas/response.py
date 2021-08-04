from pydantic import BaseModel
from typing import Optional, Any

from starlette.types import Message
from schemas.subscriber import Subscriber


class ResponseModel(BaseModel):
    message: str = "Success"
    error: Optional[str] = None
    data: Optional[Any]


class SubscriberResponseModel(ResponseModel):
    data: Subscriber


class UnsubscribedResponseModel(BaseModel):
    message: str
