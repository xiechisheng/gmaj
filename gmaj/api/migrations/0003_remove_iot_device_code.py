# Generated by Django 2.1.7 on 2020-04-26 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_iot_device'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iot_device',
            name='code',
        ),
    ]