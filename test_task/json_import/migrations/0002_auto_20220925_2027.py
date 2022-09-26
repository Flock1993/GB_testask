# Generated by Django 3.2.15 on 2022-09-25 17:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('json_import', '0001_initial'),
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
        migrations.AlterModelOptions(
            name='sensors',
            options={},
        ),
        migrations.RemoveField(
            model_name='sensors',
            name='id',
        ),
        migrations.RemoveField(
            model_name='sensors',
            name='sensor_id',
        ),
        migrations.RemoveField(
            model_name='sensors',
            name='sensor_value',
        ),
        migrations.AddField(
            model_name='sensors',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, primary_key=True, serialize=False, verbose_name='Измеряемый промежуток'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensors',
            name='values',
            field=models.JSONField(default=dict, verbose_name='Значения датчиков'),
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
