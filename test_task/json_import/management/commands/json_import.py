import json
import os
from datetime import timedelta, datetime


DIR_NAME = "telemetry"


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


def process_telemetry(conf_datetime):
    """Главная функция импорта показаний датчиков json в БД"""
    with open('config.json', newline='', encoding='utf-8') as target_sensors:
        lst_sensors = json.load(target_sensors)['loading_sensors']
        # print(lst_sensors)
        dict_sensors = {x: x for x in lst_sensors}
        mid_result = {x: {'count': 0, 'summ': 0} for x in lst_sensors}
        # print(dict_sensors)
    for json_file in os.listdir(DIR_NAME):
        if json_file.startswith('sensors_') and (json_file.endswith('.json')):
            pars_datetime = time_parsing(json_file)
            if conf_datetime <= pars_datetime < (conf_datetime + timedelta(hours=1)):
                # print(json_file)
                with open(f'{DIR_NAME}/{json_file}', newline='', encoding='utf-8') as pars_file:
                    sensors_data = json.load(pars_file)
                    # print(sensors_data['sensors'])
                    for sensor in sensors_data['sensors']:
                        if dict_sensors.get(sensor['sensor_id']) is not None:
                            # print(sensor['sensor_id'], sensor['value'])
                            mid_result[sensor['sensor_id']]['count'] += 1
                            mid_result[sensor['sensor_id']]['summ'] += sensor['value']
    result = {sensor: sensor_values['summ'] / sensor_values['count'] for sensor, sensor_values in mid_result.items() if sensor_values['count'] != 0}
    print(result)


if __name__ == '__main__':
    conf_datetime = datetime(2021, 7, 15, 10, 0, 0)
    process_telemetry(conf_datetime)
