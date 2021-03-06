# Generated by Django 2.1.7 on 2020-04-24 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_auto_20200422_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iot_device_warn',
            name='iot_device',
        ),
        migrations.DeleteModel(
            name='iot_test',
        ),
        migrations.RemoveField(
            model_name='rtsp_info',
            name='position',
        ),
        migrations.AddField(
            model_name='rtsp_info',
            name='channel_type',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='rtsp_info',
            name='inter_code_SN',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rtsp_info',
            name='manufacturer_type',
            field=models.CharField(default=0, max_length=64),
        ),
        migrations.AddField(
            model_name='rtsp_info',
            name='multicast_ip',
            field=models.CharField(default=0, max_length=64),
        ),
        migrations.AddField(
            model_name='rtsp_info',
            name='multicast_port',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rtsp_info',
            name='permissions_info',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='rtsp_info',
            name='channel',
            field=models.CharField(max_length=64),
        ),
        migrations.DeleteModel(
            name='iot_device_warn',
        ),
    ]
