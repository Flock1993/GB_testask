import json
import os

from django.core.management.base import BaseCommand

from json_import.models import Sensors


class Command(BaseCommand):
    help = 'Команда для импорта данных из .json файла в БД'

    def handle(self, *args, **options):
        """
        Запуск произвести командой python manage.py json_import
        Сейчас команда только перечисляет названия файлов из папки telemetry
        """
        dir_name = "C:/Dev/GB_testask/test_task/telemetry"
        # как задать папку относительно проекта
        for json_file in os.listdir(dir_name):
            if json_file.endswith('.json'):
                print(json_file)

        print('Импорт показаний датчиков в БД произведен успешно')

    def smoke_test_handle(self):
        """
        Здесь должен быть код который автоматически запускает команду выше
        assert ...
        """
        pass
