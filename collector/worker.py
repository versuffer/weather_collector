from celery import Celery
import os
import time


celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")


@celery_app.task(name="print_hello", ignore_result=True)
def print_hello():
    print("hello")
    time.sleep(60)
    print("world")
    return True
