import logging
from os import stat

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from fastapi import APIRouter, Body, Depends, status, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import schemas, models, crud
from db.mongodb import get_db
from core.config import settings
from core.utils import send_email, create_aliased_response


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/subscribe", response_model=schemas.ResponseModel, status_code=status.HTTP_201_CREATED)
async def add_subscriber(
    subscriber: models.SubscriberModel,
    background_tasks: BackgroundTasks,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    try:
        logger.info("in we are")
        sub = await crud.add_subscriber(db, subscriber)
        return {"data": sub}
        # JSONResponse(status_code=status.HTTP_201_CREATED)
    except Exception:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error")


@router.put("/unsubscribe/{id}", response_model=schemas.ResponseModel)
async def unsubscribe(id: str, db: AsyncIOMotorClient = Depends(get_db)):
    try:
        updated = await crud.update_subscriber_status(db, id)
        if not updated:
            raise HTTPException

        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"data": "unsubscribed"})
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="idk man")


@router.get("/getAll")
async def get_all_subs(db: AsyncIOMotorClient = Depends(get_db)):
    try:
        subs = await crud.get_all_subscribers(db)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": subs})
    except Exception:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
