from datetime import datetime
import logging
from typing import Any, List

from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from db.mongodb import AsyncIOMotorClient
from core.config import settings
from models.subscriber import SubscriberModel, SubscriberInDB

logger = logging.getLogger(__name__)


async def add_subscriber(
    db: AsyncIOMotorClient, sub: SubscriberModel
) -> SubscriberInDB:
    dbsub = SubscriberInDB(**sub.dict())
    dbsub.created_at = ObjectId(dbsub.id).generation_time
    dbsub.updated_at = ObjectId(dbsub.id).generation_time
    dbsub_encoded = jsonable_encoder(dbsub)
    row = await db[settings.DB_NAME][settings.DOCUMENT].insert_one(dbsub_encoded)
    return dbsub


async def get_all_subscribers(db: AsyncIOMotorClient) -> List[SubscriberModel]:
    logger.info(f"get all subs")
    subs = []
    rows = db[settings.DB_NAME][settings.DOCUMENT].find()
    async for row in rows:
        subs.append(row)
    return subs


async def get_subscriber_from_id(db: AsyncIOMotorClient, id: str) -> SubscriberInDB:
    row = await db[settings.DB_NAME][settings.DOCUMENT].find_one({"_id": id})
    if row:
        return SubscriberInDB(**row)


async def update_subscriber_status(db: AsyncIOMotorClient, id: str) -> int:
    row: SubscriberInDB = await get_subscriber_from_id(db, id)
    row.is_subscribed = False
    row.updated_at = datetime.utcnow()
    row_encoded = jsonable_encoder(row)
    updated = await db[settings.DB_NAME][settings.DOCUMENT].update_one(
        {"id_": str(row.id)}, {"$set": row_encoded}
    )
    return updated.matched_count
