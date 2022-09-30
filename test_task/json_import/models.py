from django.db import models


class Sensor(models.Model):
    sensor_id = models.CharField("ID датчика", max_length=15, unique=True)

    class Meta:
        verbose_name = "Датчик"
        verbose_name_plural = "Датчики"

    def __str__(self):
        return self.sensor_id


class SensorValue(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='sensor_values')
    sensor_value = models.FloatField("Показания датчика", max_length=50)
    timestamp = models.DateTimeField("Измеряемый промежуток")

    class Meta:
        verbose_name = "Значения датчика"
        verbose_name_plural = "Значения датчиков"
