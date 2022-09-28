from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)


@shared_task # позволяет определять задачи без импортирования экземпляра Celery
def import_sensor_reading():
    """Периодический импорт показаний датчиков с помощью management command"""
    call_command('jsonimport')
