from django.contrib import admin

from .models import Sensors, Sensor, SensorValue

admin.site.register(Sensors)
admin.site.register(Sensor)
admin.site.register(SensorValue)

