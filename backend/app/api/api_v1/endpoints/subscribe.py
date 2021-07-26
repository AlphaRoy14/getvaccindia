import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from fastapi import APIRouter, Body, Depends, status, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import schemas, models, crud
from db.mongodb import get_db
from core.utils import send_confirmation_email
from scripts.producer import run_mail_notif_task
from worker import format_and_send_email_worker


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
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
    response_model=schemas.SubscriberResponseModel,
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
    response_model=schemas.ResponseModel,
)
async def unsubscribe(id: str, db: AsyncIOMotorClient = Depends(get_db)):
    """
    Enable users to unsubscribe. The emails would have an unsubscribe button.
    """

    updated = await crud.update_subscriber_status(db, id)
    if not updated:
        logger.exception("unsubscribe error")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return {"data": "unsubscribed"}


@router.get("/getAll", deprecated=True)
async def get_all_subs(db: AsyncIOMotorClient = Depends(get_db)):
    """
    Get all the subscribed users for testing
    """
    try:
        subs = await crud.get_all_subscribers(db)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": subs})
    except Exception:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/triggerEmail",
    deprecated=True,
    summary="Trigger email for testing",
)
async def trigger_email():
    try:
        await run_mail_notif_task()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": "nice"})
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/runWorker", description="test function to run celery workers")
async def run_worker():
    try:
        await run_mail_notif_task()
        # await format_and_send_email_worker.delay()
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"Data": "added to the queue"}
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
