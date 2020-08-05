# Generated by Django 2.1.7 on 2020-04-22 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0062_auto_20200422_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iot_device',
            name='height',
            field=models.DecimalField(decimal_places=11, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='iot_device',
            name='latitude',
            field=models.DecimalField(decimal_places=11, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='iot_device',
            name='longitude',
            field=models.DecimalField(decimal_places=11, max_digits=14, null=True),
        ),
    ]
