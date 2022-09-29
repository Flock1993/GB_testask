import os

from django.test import TestCase

from json_import.models import Sensor, SensorValue
from json_import.script import JsonPars


class JsonImportTest(TestCase):
    DIR_DATA = 'json_import/tests/data/telemetry'
    DIR_CONF = 'json_import/tests/data'
    FILE_CONTENT = {
        'sensors_2021-24-15_10_56_18.json': ["2021-07-15 10:56:17", 1],
        'sensors_2021-07-15_10_56_18.json': ["2021-07-15 10:56:17", 2],
        'sensors_2021-07-15_10_53_18.txt': ["2021-07-15 10:53:05", 3],
    }

    def setUp(self) -> None:
        lst = [self.DIR_CONF, self.DIR_DATA]
        for elem in lst:
            if not os.path.isdir(elem):
                os.makedirs(elem)
        with open(f'{self.DIR_CONF}/config.json', 'w') as file:
            file.write('{"loading_sensors": ["sensor50", "sensor51"]}')
        for filename, value in self.FILE_CONTENT.items():
            with open(f'{self.DIR_DATA}/{filename}', 'w') as file:
                file.write('{"timestamp": '
                           f'"{value[0]}",'
                           '"sensors": [{"sensor_id": "sensor50", "value": '
                           f'{value[1]}'
                           '}, {"sensor_id": "sensor51", "value": '
                           f'{value[1]}'
                           '}]}')
        with open(f'{self.DIR_DATA}/sensors_2021-07-15_10_55_44.csv', 'w') as file:
            file.write('"timestamp","2021-07-15 10:56:17",'
                       '"sensor50",4,"sensor51",4')

    def tearDown(self) -> None:
        flag = True
        if flag:
            for file in os.listdir(self.DIR_DATA):
                os.remove(os.path.join(self.DIR_DATA, file))
            try:
                os.remove(os.path.join(self.DIR_CONF, 'config.json'))
            except OSError:
                pass

    def test_smoke(self) -> None:
        """База данных наполняется корректными значениями"""
        instanse = JsonPars(dir_config=self.DIR_CONF,
                            dir_telemetry=self.DIR_DATA)
        instanse.process_telemetry()
        sensor50 = Sensor.objects.get(sensor_id='sensor50')
        self.assertEqual(sensor50.sensor_values.count(), 1)
        sensor_value50 = sensor50.sensor_values.last()
        self.assertEqual(sensor_value50.sensor_value, 2)

    def test_bad_filename(self) -> None:
        """Файлы с некорректным названием и форматом не обрабатываются"""
        instanse = JsonPars(dir_config=self.DIR_CONF,
                            dir_telemetry=self.DIR_DATA)
        instanse.process_telemetry()
        sensor50 = Sensor.objects.get(sensor_id='sensor50')
        sensor_value50 = sensor50.sensor_values.last()
        self.assertEqual(sensor_value50.sensor_value, 0)

    def test_bad_datetime(self) -> None:
        """Функция parsing_datetime не обрабатывает некорректную дату"""
        pass

    def test_create_collections(self):
        """Вспомогательные коллекции создаются"""
        pass

    def test_delta_datetime(self):
        """Корректная работа функции delta_datetime"""
        pass
