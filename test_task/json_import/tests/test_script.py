import os

from django.test import TestCase

from json_import.models import Sensor, SensorValue
from json_import.script import JsonPars


class JsonImportTest(TestCase):
    DIR_DATA = 'json_import/tests/data/telemetry'
    DIR_CONF = 'json_import/tests/data'

    def setUp(self) -> None:
        lst = [self.DIR_CONF, self.DIR_DATA]
        for elem in lst:
            if not os.path.isdir(elem):
                os.makedirs(elem)
        with open(f'{self.DIR_CONF}/config.json', 'w') as file:
            file.write('{"loading_sensors": ["sensor50", "sensor51"]}')
        # файл с некорректной датой
        with open(f'{self.DIR_DATA}/sensors_2021-24-15_10_53_05.json', 'w') as file:
            file.write('{"timestamp": "2021-07-15 10:53:05", '
                       '"sensors": [{"sensor_id": "sensor50", "value": 1},'
                       ' {"sensor_id": "sensor51", "value": 1}]}')
        # файлы с некорректным форматом
        with open(f'{self.DIR_DATA}/sensors_2021-07-15_10_55_44.txt', 'w') as file:
            file.write('{"timestamp": "2021-07-15 10:55:43", "sensors": '
                       '[{"sensor_id": "sensor50", "value": 2}, '
                       '{"sensor_id": "sensor51", "value": 2}]}')
        with open(f'{self.DIR_DATA}/sensors_2021-07-15_10_56_18.csv', 'w') as file:
            file.write('"2021-07-15 10:56:17","sensor50",3,"sensor51",3')
        # корректный файл
        with open(f'{self.DIR_DATA}/sensors_2021-07-15_10_57_55.json', 'w') as file:
            file.write('{"timestamp": "2021-07-15 10:57:54", "sensors": '
                       '[{"sensor_id": "sensor50", "value": 4}, '
                       '{"sensor_id": "sensor51", "value": 4}]}')

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

        print(Sensor.objects.all)
        #sensor50 = Sensor.objects.get(sensor_id='sensor50')
        #sensor_value50 = sensor50.sensor_values.last()
