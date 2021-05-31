from typing import Any, List, Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr


class Subscriber(BaseModel):
    email: EmailStr
    zipcode: Optional[int]
    district_id: Optional[int]
    vaccine_type: int
