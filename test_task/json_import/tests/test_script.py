import os

from django.test import TestCase

from json_import.models import Sensor
from json_import.script import JsonPars, parsing_datetime, delta_datetime
from datetime import datetime


class JsonImportTest(TestCase):
    DIR_DATA = 'json_import/tests/data/telemetry'
    DIR_CONF = 'json_import/tests/data'

    def setUp(self) -> None:
        lst = [self.DIR_CONF, self.DIR_DATA]
        for elem in lst:
            if not os.path.isdir(elem):
                os.makedirs(elem)

    def tearDown(self) -> None:
        flag = False
        if flag:
            for file in os.listdir(self.DIR_DATA):
                os.remove(os.path.join(self.DIR_DATA, file))
            try:
                os.remove(os.path.join(self.DIR_CONF, 'config.json'))
            except OSError:
                pass

    def test_smoke(self) -> None:
        """Smoke test"""
        instanse = JsonPars()
        instanse.process_telemetry()
        lst = instanse.create_collections()[0]
        self.assertEqual(Sensor.objects.count(), len(lst))
        sensor24 = Sensor.objects.get(sensor_id='sensor24')
        sensor_value24 = sensor24.sensor_values.last()
        self.assertEqual(sensor_value24.sensor_value, 0.405)

    def test_bad_datetime(self) -> None:
        """Функция parsing_datetime не обрабатывает некорректную дату"""
        vat_datetime = parsing_datetime('sensors_2021-24-99_10_53_05.json')
        self.assertEqual(vat_datetime, None)

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
        instanse.process_telemetry()
        lst_sensors, dict_sensors, mid_result = instanse.create_collections()
        length = 6
        self.assertEqual(len(lst_sensors), length)
        self.assertEqual(len(dict_sensors), length)
        self.assertEqual(len(mid_result), length)

    def test_bad_filename(self) -> None:
        """Файлы с некорректным названием и форматом не обрабатываются"""
        pass

    def test_bad_datetime(self) -> None:
        """Файлы с некорректной датой не обрабатываются"""
        pass
