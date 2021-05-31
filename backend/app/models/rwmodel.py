from datetime import datetime, timezone, tzinfo

from pydantic import BaseModel, BaseConfig
from bson import ObjectId


class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        arbitary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
        }
