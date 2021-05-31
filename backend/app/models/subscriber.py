from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

from models.dbmodel import DBModelMixin, PyObjectId
from models.rwmodel import RWModel


class SubscriberModel(RWModel):
    name: Optional[str]
    email: EmailStr
    state: Optional[str]
    district_id: Optional[str]
    zip_code: Optional[str]
    is_subscribed: bool = True


class SubscriberInDB(SubscriberModel, DBModelMixin):
    pass
    # id : PyObjectId = Field(default_factory=PyObjectId, alias="_id")
