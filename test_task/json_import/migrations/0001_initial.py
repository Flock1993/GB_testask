# Generated by Django 3.2.15 on 2022-09-28 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.CharField(max_length=15, unique=True, verbose_name='ID датчика')),
            ],
            options={
                'verbose_name': 'Датчик',
                'verbose_name_plural': 'Датчики',
            },
        ),
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('timestamp', models.DateTimeField(editable=False, primary_key=True, serialize=False, verbose_name='Измеряемый промежуток')),
                ('values', models.JSONField(default=dict, verbose_name='Значения датчиков')),
            ],
        ),
        migrations.CreateModel(
            name='SensorValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_value', models.FloatField(max_length=50, verbose_name='Показания датчика')),
                ('timestamp', models.DateTimeField(verbose_name='Измеряемый промежуток')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_values', to='json_import.sensor')),
            ],
            options={
                'verbose_name': 'Значения датчика',
                'verbose_name_plural': 'Значения датчиков',
            },
        ),
    ]
