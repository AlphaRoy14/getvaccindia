import asyncio
import os
from pydantic.main import BaseConfig
import requests
from typing import Dict, List
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dateutil import tz

from db.mongodb import get_db
from db.mongodb_utils import connect_to_mongo
from core.utils import format_and_send_email
from core.config import settings
from worker import format_and_send_email_worker


async def get_unique_zipcodes() -> List:
    db = await get_db()
    zipcode_list = await db[settings.DB_NAME][settings.DOCUMENT].distinct("zip_code")
    return zipcode_list


async def get_emails_of_users(zip_code: int, doze: List[int]) -> List[Dict]:
    """
    Get emails of users with a particular zipcode and vaccine doze
    """
    db = await get_db()
    emails = db[settings.DB_NAME][settings.DOCUMENT].find(
        {"zip_code": zip_code, "vaccine_doze": {"$all": doze}}, {"email": 1}
    )
    return emails


def make_get_request(zipcode):
    # TODO make this async
    now = datetime.now()
    india_tz = tz.gettz("Asia/Kolkata")
    now.replace(tzinfo=india_tz)
    date = now.strftime("%d-%m-%Y")
    headers = {
        "Accept-Language": "en_US",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    }
    url = str(settings.SETU_API_ZIPCODE) + f"?pincode={zipcode}&date={date}"
    print(f"URL IS {url}")
    response = requests.get(url, headers=headers)
    return response.json()


def filter_vaccine_data(vaccine_data: List[Dict]):

    doze1_filter = list(
        filter(lambda x: int(x["available_capacity_dose1"]) > 0, vaccine_data)
    )
    doze2_filter = list(
        filter(lambda x: int(x["available_capacity_dose2"]) > 0, vaccine_data)
    )
    # both_doze = list(set.intersection(set(doze1_filter), set(doze2_filter)))
    return (doze1_filter, doze2_filter)


async def email_users(data: List, id_emails: Dict, subject):

    # since heroku is paid for more than 2 dynos 😭 we arent running workers on heroku
    celery_workers = os.environ.get("CELERY_WORKERS", "True") == "True"
    formated_data = list(
        map(
            lambda x: {
                "Vaccine": x["vaccine"],
                "Name": x["name"],
                "Address": x["address"],
                "District Name": x["district_name"],
                "Min age limit": x["min_age_limit"],
            },
            data,
        )
    )

    async for item in id_emails:
        id = item["_id"]
        email = item["email"]
        if celery_workers:
            format_and_send_email_worker.delay(
                email=[email], template_data=formated_data, user_id=id, subject=subject
            )
        else:
            await format_and_send_email(
                email=[email], template_data=formated_data, user_id=id, subject=subject
            )


async def run_mail_notif_task():
    """
    Entry point to run the emailing job
    """
    # connecting to mongo
    await connect_to_mongo()

    zip_codes = await get_unique_zipcodes()
    for zipcode in zip_codes:
        vaccine_data = make_get_request(zipcode)
        if not vaccine_data:
            continue
        doze1, doze2 = filter_vaccine_data(vaccine_data["sessions"])
        if doze1:
            id_email_doze1 = await get_emails_of_users(zipcode, [1])
            await email_users(
                doze1, id_email_doze1, subject="Covid vaccine doze 1 available"
            )
        if doze2:
            id_email_doze2 = await get_emails_of_users(zipcode, [2])
            await email_users(
                doze2, id_email_doze2, subject="Covid vaccine doze 2 available"
            )


if __name__ == "__main__":
    asyncio.run(run_mail_notif_task())
