# Generated by Django 2.1.7 on 2019-10-22 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20191022_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rtsp_server',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
