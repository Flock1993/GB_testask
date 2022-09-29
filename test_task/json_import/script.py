import json
import os
from datetime import datetime, timedelta
from decimal import *
from typing import Dict, List, Optional, Tuple

from json_import.models import Sensor, SensorValue


def parsing_datetime(file_name) -> datetime:
    """Парсинг даты и времени в названии файла"""
    strt: int = file_name.find('_')
    nd: int = file_name.find('_', strt + 1)
    year, month, day = file_name[strt + 1:nd].split('-')

    strt = nd
    nd: int = file_name.find('.')
    hours, minutes, seconds = file_name[strt + 1:nd].split('_')

    try:
        return datetime(int(year), int(month), int(day),
                        int(hours), int(minutes), int(seconds))
    except ValueError:
        return None


def delta_datetime(str_data: str, pars_datetime: datetime
                   ) -> Optional[datetime]:
    """
    Отладочная функция расчета разницы datatime имени файла и содержимого
    Дата в названии файла и его содержимом отличается
    """
    content_data = datetime.strptime(str_data, '%Y-%m-%d %H:%M:%S')
    if pars_datetime != content_data:
        return pars_datetime - content_data
    return None


class JsonPars:
    """Передача показаний датчиков"""

    DIR_TELEM = 'data/telemetry'
    DIR_CONFIG = 'data'
    REF_POINT = datetime(2021, 7, 15, 10, 0, 0)
    # для "боевого" применения класса использовать datetime.now()

    def __init__(self,
                 dir_config: str = DIR_CONFIG,
                 dir_telemetry: str = DIR_TELEM,
                 conf_datetime: datetime = REF_POINT,
                 ) -> None:
        self.dir_telemetry = dir_telemetry
        self.dir_config = dir_config
        self.conf_datetime = conf_datetime

    def create_collections(
            self) -> Tuple[List[str], Dict[str, str], Dict[str, int]]:
        """
        Создание объектов и вспомогательных коллекций
        из названий целевых датчиков
        """
        with open(f'{self.dir_config}/config.json', encoding='utf-8') as target_sensors:
            lst_sensors = json.load(target_sensors)['loading_sensors']
            # ['sensor1', 'sensor5', 'sensor6', ...] # print(lst_sensors)
            for elem in lst_sensors:
                Sensor.objects.get_or_create(sensor_id=elem)
            dict_sensors = {x: x for x in lst_sensors}
            mid_result = {x: {'count': 0, 'summ': 0} for x in
                          lst_sensors}  # "sensor1": [0, 0]
            # {'sensor1': 'sensor1', ...} print(dict_sensors)
        return lst_sensors, dict_sensors, mid_result

    def process_telemetry(self) -> None:
        """Передача показаний датчиков в БД"""
        lst_sensors, dict_sensors, mid_result = self.create_collections()
        for json_file in os.listdir(self.dir_telemetry):
            if not ((json_file.startswith('sensors_') or (
                    json_file.endswith('.json')) or len(json_file) == 32)):
                print(f'Название или формат файла {json_file} некорректны')
            else:
                proces_datetime = parsing_datetime(json_file)
                if proces_datetime is not None:
                    if self.conf_datetime <= proces_datetime < (
                            self.conf_datetime + timedelta(hours=1)):
                        with open(f'{self.dir_telemetry}/{json_file}',
                                  encoding='utf-8') as pars_file:
                            sensors_data = json.load(pars_file)
                            for sensor in sensors_data['sensors']:
                                if dict_sensors.get(
                                        sensor['sensor_id']) is not None:
                                    mid_result[sensor['sensor_id']][
                                        'count'] += 1
                                    mid_result[sensor['sensor_id']]['summ'] \
                                        += sensor['value']
                else:
                    return False
        result = {}
        for sensor, sensor_values in mid_result.items():
            if sensor_values['count'] == 0:
                result[sensor] = 0
            else:
                result[sensor] = Decimal(
                    sensor_values['summ'] / sensor_values['count']).quantize(
                    Decimal('1.000'))
        for sens, value in result.items():
            SensorValue.objects.get_or_create(
                sensor=Sensor.objects.get(sensor_id=sens),
                sensor_value=value,
                timestamp=self.conf_datetime
            )
        print(f'Импорт показаний датчиков выполнен успешно {result}')
        return True
