from .service import send

from celery import shared_task

@shared_task
def send_email_task():
    send()
