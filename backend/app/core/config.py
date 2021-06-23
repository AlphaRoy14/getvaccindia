import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator
from ipaddress import IPv4Address, collapse_addresses


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    BACKEND_CORS_ORIGINS: Union[str, List[str]] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    MONGODB_URL: str
    DB_NAME: str
    DOCUMENT: str

    # mail config ✉️
    MAIL_USERNAME: str
    MAIL_FROM: EmailStr
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    # unsubscribe base
    UNSUBSCRIBE_BASE: Optional[AnyHttpUrl]

    # Setu API
    SETU_API_ZIPCODE: AnyHttpUrl

    # Celery
    CELERY_BROKER_URL: Optional[str]
    CELERY_RESULT_BACKEND: Optional[str]

    class Config:
        case_sensitive = True


settings = Settings(_env_file=".env")
