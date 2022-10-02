import os
from datetime import datetime

from django.test import TestCase

from json_import.models import Sensor, SensorValue
from json_import.script import JsonPars, delta_datetime


class JsonImportTest(TestCase):
    DIR_DATA = 'json_import/tests/data/telemetry'
    DIR_CONF = 'json_import/tests/data'

    def setUp(self) -> None:
        lst = [self.DIR_CONF, self.DIR_DATA]
        for elem in lst:
            if not os.path.isdir(elem):
                os.makedirs(elem)
        with open(f'{self.DIR_CONF}/config.json', 'w') as file:
            file.write(
                '{"loading_sensors": ["sensor50", "sensor51", "sensor52"]}')

    def tearDown(self) -> None:
        # отладочная переменная flag, True для удаления тестовых файлов
        flag = True
        if flag:
            for file in os.listdir(self.DIR_DATA):
                os.remove(os.path.join(self.DIR_DATA, file))
            try:
                os.remove(os.path.join(self.DIR_CONF, 'config.json'))
            except OSError:
                pass

    def test_bad_datetime(self) -> None:
        """Файлы с некорректным форматом даты в названнии не обрабатываются"""
        with open(f'{self.DIR_DATA}/sensors_2021-99-15_10_55_44.json', 'w') as file:
            file.write('{"timestamp": "2021-07-15 17:55:43", "sensors": '
                       '[{"sensor_id": "sensor52", "value": 0.314}]}')
        instanse = JsonPars(
            dir_config=self.DIR_CONF,
            dir_telemetry=self.DIR_DATA,
        )

        instanse.process_telemetry()
        boolean = SensorValue.objects.filter(sensor_value=0.314).exists()

        self.assertEqual(boolean, False)

    def test_smoke(self) -> None:
        """Smoke test"""
        instanse = JsonPars()

        instanse.process_telemetry()
        lst = instanse.create_collections()[0]
        sensor24 = Sensor.objects.get(sensor_id='sensor24')
        sensor_value24 = sensor24.sensor_values.last()

        self.assertEqual(Sensor.objects.count(), len(lst))
        self.assertEqual(sensor_value24.sensor_value, 0.405)

    def test_delta_datetime(self):
        """Корректная работа функции delta_datetime"""
        str_datatime = "2021-07-15 10:53:05"
        datetime_equal = datetime(2021, 7, 15, 10, 53, 5)
        datetime_diff = datetime(2021, 7, 15, 10, 59, 5)

        equal = delta_datetime(str_datatime, datetime_equal)
        diff = delta_datetime(str_datatime, datetime_diff)

        self.assertEqual(equal, None)
        self.assertEqual(str(diff), '0:06:00')

    def test_create_collections(self):
        """Вспомогательные коллекции создаются"""
        instanse = JsonPars()
        # В файле config.json находится список с шестью названиями датчиков
        length = 6

        instanse.process_telemetry()
        lst_sensors, dict_sensors, mid_result = instanse.create_collections()

        self.assertEqual(len(lst_sensors), length)
        self.assertEqual(len(dict_sensors), length)
        self.assertEqual(len(mid_result), length)

    def test_bad_filename(self) -> None:
        """Файлы с некорректным форматом не обрабатываются"""
        with open(f'{self.DIR_DATA}/sensors_2021-07-15_10_55_44.txt', 'w') as file:
            file.write('{"timestamp": "2021-07-15 10:55:43", "sensors": '
                       '[{"sensor_id": "sensor50", "value": 2}, '
                       '{"sensor_id": "sensor51", "value": 2}]}')
        with open(f'{self.DIR_DATA}/sensors_2021-07-15_10_56_18.csv',
                  'w') as file:
            file.write('"2021-07-15 10:56:17","sensor50",3,"sensor51",3')
        instanse = JsonPars(
            dir_config=self.DIR_CONF,
            dir_telemetry=self.DIR_DATA
        )

        instanse.process_telemetry()
        incorrect = [2, 3, 2.5]
        sensor51 = Sensor.objects.get(sensor_id='sensor51')
        sensor_value51 = sensor51.sensor_values.last()

        self.assertNotIn(sensor_value51.sensor_value, incorrect)

    def test_datetime_outofrange(self) -> None:
        """
        Данные из файлов с датой вне диапазона считывания не попадают в БД
        """
        with open(f'{self.DIR_DATA}/sensors_2021-07-15_17_55_44.json', 'w') as file:
            file.write('{"timestamp": "2021-07-15 17:55:43", "sensors": '
                       '[{"sensor_id": "sensor50", "value": 1}, '
                       '{"sensor_id": "sensor51", "value": 2}]}')
        native_datatime = datetime(2021, 7, 15, 13, 0, 0)
        instanse = JsonPars(
            dir_config=self.DIR_CONF,
            dir_telemetry=self.DIR_DATA,
            conf_datetime=native_datatime
        )

        instanse.process_telemetry()
        sensor51 = Sensor.objects.get(sensor_id='sensor51')
        sensor_value51 = sensor51.sensor_values.last()

        self.assertNotEqual(sensor_value51.sensor_value, 2)
