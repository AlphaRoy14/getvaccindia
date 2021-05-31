import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Host

from api.api_v1.api import api_router
from db.mongodb_utils import connect_to_mongo, close_mongo_connection
from core.config import settings

import uvicorn

logging.basicConfig(
    filename="fastapi.log",
    format="[%(asctime)s] — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
    level=logging.DEBUG,
)
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Apis to subscribe and unsubscribe users from the mailing list",
)
app.include_router(api_router, prefix=settings.API_V1_STR)

# 😇 Set all cors enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
