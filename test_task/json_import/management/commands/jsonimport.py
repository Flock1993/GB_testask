from django.core.management.base import BaseCommand
from json_import.script import JsonPars


class Command(BaseCommand):
    help = 'Команда для импорта показаний датчиков из .json файла в БД'

    def handle(self, *args, **options):
        """
         Запуск произвести командой python manage.py jsonimport_rev1
         """
        instanse = JsonPars()
        instanse.process_telemetry()
        # для боевого применения в JsonPars передать атрибут
        # conf_datetime = datetime.now() отбросив миллисекунды
