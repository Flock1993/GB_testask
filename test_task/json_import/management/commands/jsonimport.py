import json
import os
from datetime import timedelta, datetime
from decimal import *

from django.core.management.base import BaseCommand

from json_import.models import SensorValue, Sensor

DIR_TELEM = 'data/telemetry'
DIR_CONFIG = 'data/config.json'


def adjust():
    """Функция передачи начала отсчета в management command для ручной отладки"""
    return datetime(2021, 7, 15, 10, 0, 0)


def time_parsing(file_name):
    """Парсинг даты и времени в названии файла"""
    strt = file_name.find('_')
    nd = file_name.find('_', strt + 1)
    year, month, day = file_name[strt + 1:nd].split('-')

    strt = nd
    nd = file_name.find('.')
    hours, minutes, seconds = file_name[strt + 1:nd].split('_')

    return datetime(int(year), int(month), int(day),
                    int(hours), int(minutes), int(seconds))


class Command(BaseCommand):
    help = 'Команда для импорта показаний датчиков из .json файла в БД, развернутую на Docker'

    def handle(self, *args, **options):
        """
        Запуск произвести командой python manage.py jsonimport
        """
        # создание списка и словарей с целевыми датчиками
        with open(DIR_CONFIG, encoding='utf-8') as target_sensors:
            lst_sensors = json.load(target_sensors)['loading_sensors']
            # ['sensor1', 'sensor5', 'sensor6', ...] # print(lst_sensors)
            for elem in lst_sensors:
                Sensor.objects.get_or_create(sensor_id=elem)
            dict_sensors = {x: x for x in lst_sensors}
            mid_result = {x: {'count': 0, 'summ': 0} for x in
                          lst_sensors}  # "sensor1": [0, 0]
            # {'sensor1': 'sensor1', ...} print(dict_sensors)
        conf_datetime = adjust()
        for json_file in os.listdir(DIR_TELEM):
            if json_file.startswith('sensors_') and (
                    json_file.endswith('.json')):
                pars_datetime = time_parsing(json_file)
                if conf_datetime <= pars_datetime < (
                        conf_datetime + timedelta(hours=1)):
                    with open(f'{DIR_TELEM}/{json_file}', encoding='utf-8') as pars_file:
                        sensors_data = json.load(pars_file)
                        for sensor in sensors_data['sensors']:
                            if dict_sensors.get(
                                    sensor['sensor_id']) is not None:
                                mid_result[sensor['sensor_id']]['count'] += 1
                                mid_result[sensor['sensor_id']]['summ'] += \
                                    sensor['value']
        getcontext().prec = 10
        result = {sensor: Decimal(sensor_values['summ'] / sensor_values['count']).quantize(Decimal('1.000')) for
                  sensor, sensor_values in mid_result.items() if
                  sensor_values['count'] != 0}
        for sens, value in result.items():
            SensorValue.objects.get_or_create(
                sensor=Sensor.objects.get(sensor_id=sens),
                sensor_value=value,
                timestamp=conf_datetime
            )
        print(result)
        print('Импорт показаний датчиков выполнен успешно')
