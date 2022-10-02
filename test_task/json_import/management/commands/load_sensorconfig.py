import json

from django.core.management.base import BaseCommand

from json_import.models import Sensor


class Command(BaseCommand):
    help = 'Вспомогательная команда для импорта config.json файла в БД'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--file',
            default='data/config.json',
            help='Путь до файла config.json для загрузки целевых сенсоров',
        )

    def handle(self, file, *args, **options):
        """Импорт целевых датчиков перед выполнением POST запросов"""
        with open(file, encoding='utf-8') as target_sensors:
            sensors = json.load(target_sensors)['loading_sensors']
            for elem in sensors:
                Sensor.objects.get_or_create(sensor_id=elem)
        self.stdout.write(self.style.SUCCESS(
            'Целевые датчики успешно загружены'))
