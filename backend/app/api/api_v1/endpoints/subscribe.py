import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from fastapi import APIRouter, Body, Depends, status, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import schemas, models, crud
from db.mongodb import get_db
from core.utils import send_confirmation_email
from scripts.producer import run


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/email")
async def get_email():
    """
    Just a test api for mailing service

    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="just a test api"
    )
    await send_confirmation_email(
        email=["alpharoy14@gmail.com"],
        template_data={
            "name": "Arindaam",
            "state": "west bengal",
            "age": 23,
            "vaccine doze": 2,
        },
    )
    return {"message": "sent"}


@router.post(
    "/subscribe",
    response_model=schemas.SubscriberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_subscriber(
    subscriber: models.SubscriberModel,
    background_tasks: BackgroundTasks,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    try:
        email_body = schemas.SubscriberEmailBody(**subscriber.dict())
        sub = await crud.add_subscriber(db, subscriber)
        background_tasks.add_task(
            send_confirmation_email,
            [subscriber.email],
            email_body.dict(exclude_none=True),
            str(sub.id),
        )
        return {"data": sub}
    except Exception:
        HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )


@router.put(
    "/unsubscribe/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.SubscriberResponse,
)
async def unsubscribe(id: str, db: AsyncIOMotorClient = Depends(get_db)):
    """
    Enable users to unsubscribe. The emails would have an unsubscribe button.
    """
    try:
        updated = await crud.update_subscriber_status(db, id)
        if not updated:
            raise HTTPException
        return {"data": "unsubscribed"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed"
        )


@router.get("/getAll")
async def get_all_subs(db: AsyncIOMotorClient = Depends(get_db)):
    """
    Get all the subscribed users for testing
    """
    try:
        subs = await crud.get_all_subscribers(db)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": subs})
    except Exception:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/triggerEmail")
async def trigger_email():
    try:
        await run()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": "nice"})
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
