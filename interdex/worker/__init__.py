from celery import Celery
from interdex import get_config

app = Celery('tasks', broker=get_config().get("broker_url"))

from .report_world_tasks import report_world
# app.autodiscover_tasks(
#    ['interdex.worker.report_world_tasks']
# )
