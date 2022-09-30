from rest_framework import serializers


class SensorValueSerializer(serializers.Serializer):
    sensor_id = serializers.CharField()
    value = serializers.FloatField()


class WriteSensorValuesSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    sensor_values = SensorValueSerializer(many=True)

    def save(self, **kwargs):
        print(self.validated_data)
        timestamp = self.validated_data['timestamp']
        values = self.validated_data['sensor_values']


