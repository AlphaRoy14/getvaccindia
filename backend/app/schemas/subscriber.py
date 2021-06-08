from typing import Any, List, Optional
from pydantic import BaseModel, validator
from pydantic.error_wrappers import ValidationError
from pydantic.networks import EmailStr


class SubscriberEmailBody(BaseModel):
    name: Optional[str]
    email: EmailStr
    state: Optional[str]
    district: Optional[str]
    zip_code: Optional[int]
    district_id: Optional[int]
    # str so that it can be joined
    vaccine_doze: List[str] = [1, 2]

    @validator("vaccine_doze")
    def set_vaccine_doze_to_str(cls, v):
        if isinstance(v, list):
            return ", ".join(v)
        raise ValueError(v)


class Subscriber(SubscriberEmailBody):
    email: EmailStr
