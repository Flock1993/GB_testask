from rest_framework import serializers
from json_import.models import SensorValue, Sensor


class SensorValueSerializer(serializers.Serializer):
    sensor_id = serializers.CharField()
    value = serializers.DecimalField(max_digits=10, decimal_places=3)


class WriteSensorValuesSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    sensor_values = SensorValueSerializer(many=True)

    def validate(self, attrs):
        timestamp = attrs['timestamp']
        if SensorValue.objects.filter(timestamp__gte=timestamp).exists():
            raise serializers.ValidationError({'timestamp': 'Невалидная дата'})
        return attrs

    def save(self):
        timestamp = self.validated_data['timestamp']
        values = self.validated_data['sensor_values']
        existed_sensors = set(
            list(Sensor.objects.values_list('sensor_id', flat=True)))
        sensor_names = set([sensor['sensor_id'] for sensor in values])
        difference = sensor_names.difference(existed_sensors)
        bulk_objs = []
        for sensor_value in values:
            if sensor_value['sensor_id'] in difference:
                continue
            bulk_objs.append(SensorValue(
                sensor=Sensor.objects.get(sensor_id=sensor_value['sensor_id']),
                sensor_value=sensor_value['value'],
                timestamp=timestamp,
            ))
        SensorValue.objects.bulk_create(bulk_objs)
        return list(difference)




