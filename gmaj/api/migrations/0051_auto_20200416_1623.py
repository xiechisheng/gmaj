# Generated by Django 2.1.7 on 2020-04-16 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20200415_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='iot_device',
            name='device_brand_name',
            field=models.CharField(default=0, max_length=64),
        ),
        migrations.AddField(
            model_name='iot_device',
            name='device_type_name',
            field=models.CharField(default=0, max_length=64),
        ),
        migrations.AlterField(
            model_name='iot_device',
            name='iot_address',
            field=models.CharField(default=0, max_length=256),
        ),
    ]
