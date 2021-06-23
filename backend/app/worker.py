import os
import time
import asyncio

from asgiref.sync import async_to_sync

from typing import Dict, List

from core.config import settings
from celery import Celery
from core.utils import format_and_send_email
from core.celery_app import celery_app


@celery_app.task(acks_late=True)
def format_and_send_email_worker(
    email: List, template_data: List[Dict], user_id: str, subject: str
):
    print("SENDING MAIL WORKER TASK")
    async_to_sync(format_and_send_email)(email, template_data, user_id, subject)
