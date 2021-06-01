from typing import Any, List, Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr


class SubscriberEmailBody(BaseModel):
    name: Optional[str]
    email: EmailStr
    zip_code: Optional[int]
    district_id: Optional[int]
    vaccine_doze: int = 3


class Subscriber(SubscriberEmailBody):
    email: EmailStr
