# Generated by Django 2.1.7 on 2019-10-24 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_iot_device_generic_plan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='iot_device',
            old_name='type',
            new_name='type_name',
        ),
        migrations.AddField(
            model_name='iot_device',
            name='type_int',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
