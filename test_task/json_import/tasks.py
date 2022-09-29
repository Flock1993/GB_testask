from test_task.celery import app
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)


@app.task
def import_sensor_reading():
    """Периодический импорт показаний датчиков с помощью management command"""
    call_command('jsonimport')
