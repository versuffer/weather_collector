from celery import Celery
import os
import time


celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery_app.conf.beat_schedule = {
    'print_hello': {
        'task': 'print_hello',
        'schedule': 10.0,
    },
}
celery_app.conf.timezone = 'UTC'


@celery_app.task(name="print_hello", ignore_result=True)
def print_hello():
    print("hello")
    return True
