from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from json_import.models import SensorValue, Sensor
from django.db.models import Max
from datetime import datetime

from . import serializers


class WriteSensorValuesView(GenericAPIView):
    serializer_class = serializers.WriteSensorValuesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # поиск минимума datetime в БД
        sensorvalue = SensorValue.objects.all()
        datetime_db = sensorvalue.aggregate(Max('timestamp'))['timestamp__max']
        print(datetime_db, type(datetime_db))

        # парсинг даты из запроса
        datetime_request_str = request.data['timestamp'][:-5]
        datetime_request = datetime.strptime(datetime_request_str,
                                             '%Y-%m-%dT%H:%M:%S')
        print(datetime_request, type(datetime_request))

        # создание списка названий датчиков из БД
        db_sensor_lst = list(Sensor.objects.all().values_list('sensor_id'))
        print(db_sensor_lst, type(db_sensor_lst))


        # парсинг названий датчиков из запроса
        request_sensor_lst = request.data['sensor_values']
        # print(request.data['sensor_values'])

        # имя датчика в запросе есть в БД
        for request_sensor in request_sensor_lst:
            if request_sensor in db_sensor_lst:
                print(request_sensor, 'sensor name in DB')

        if datetime_request < datetime_db:
            return JsonResponse(
                {'status': 'Error',
                 'desc': 'timestamp меньше чем максимальный timestamp в БД'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_200_OK)
