from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

import logging
from core.config import settings

logger = logging.getLogger(__name__)


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_db() -> AsyncIOMotorDatabase:
    """We need to only connect to a single database 🙃"""
    return db.client
