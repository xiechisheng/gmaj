# Generated by Django 2.1.7 on 2019-10-30 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_rtsp_rolling'),
    ]

    operations = [
        migrations.CreateModel(
            name='rtsp_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipc', models.IntegerField(default=0)),
                ('user', models.IntegerField(default=0)),
                ('record_code', models.CharField(max_length=64)),
                ('type', models.PositiveSmallIntegerField(default=1)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
