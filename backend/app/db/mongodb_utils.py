import logging

from motor.motor_asyncio import AsyncIOMotorClient

from db.mongodb import db
from core.config import settings


async def connect_to_mongo():
    logging.info("Connecting to mongo...")
    db.client = AsyncIOMotorClient(str(settings.MONGODB_URL))
    logging.info("DB connected!")


async def close_mongo_connection():
    logging.info("Closing DB connection...")
    db.client.close()
    logging.info("DB closed!")
