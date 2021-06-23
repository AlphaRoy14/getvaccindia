from scripts.producer import run_mail_notif_task
from core.celery_app import celery_app
from asgiref.sync import async_to_sync


@celery_app.task(acks_late=True, name="send_notification")
def send_notification():
    """
    Need to convert the async function to sync since celery does not support it yet
    """
    async_to_sync(run_mail_notif_task)()


print(f"THE NAME OF THE TAsk IS {send_notification.name}")
celery_app.conf.beat_schedule = {
    "Email-every-30-sec-task": {"task": "send_notification", "schedule": 30.0}
}
