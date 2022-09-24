from django.db import models


class Sensors(models.Model):
    sensor_id = models.CharField("ID датчика", max_length=15, unique=True)
    sensor_value = models.FloatField("Показания датчика", max_length=50)

    class Meta:
        verbose_name = "Датчик"
        verbose_name_plural = "Датчики"

    def __str__(self):
        return self.sensor_id
