# %%
import logging
import os
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Body
from fastapi_mail.config import ConnectionConfig
from jinja2 import Environment, FileSystemLoader

from jinja2.nodes import Output
from pydantic import BaseModel
from fastapi import Depends
from fastapi.responses import JSONResponse
from typing import Dict, List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic.networks import EmailStr, HttpUrl
from core.config import settings

logger = logging.getLogger(__name__)


def create_aliased_response(model: BaseModel, status_code) -> JSONResponse:
    return JSONResponse(
        status_code=status_code, content=jsonable_encoder(model, by_alias=True)
    )


mail_conf = ConnectionConfig(
    MAIL_USERNAME="getvaccindia",
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM="getvaccindia@gmail.com",
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)

# file_loader = FileSystemLoader("backend/app/email-template/")
file_loader = FileSystemLoader("email-template/")
env = Environment(loader=file_loader)

fm = FastMail(mail_conf)


async def send_email(email: List[EmailStr], body, subject):
    message = MessageSchema(
        subject=subject, recipients=email, body=body, subtype="html"
    )
    await fm.send_message(message)


async def send_confirmation_email(
    email: List[EmailStr], template_data: Dict, user_id: str
):
    # TODO change user_id to slug

    unsub_url = settings.UNSUBSCRIBE_BASE + user_id
    template = env.get_template("confirmation.html")
    output = template.render(data=template_data, unsub=unsub_url)
    await send_email(
        email=email, body=output, subject="getvaccindia email subscription"
    )


async def format_and_send_email(
    email: List[EmailStr], template_data: List[Dict], user_id: str, subject: str
):
    # TODO remove template file
    unsub_url = settings.UNSUBSCRIBE_BASE + user_id
    template = env.get_template("notification.html")
    output = template.render(data=template_data, unsub=unsub_url)
    await send_email(email=email, body=output, subject=subject)
