# Generated by Django 2.1.7 on 2019-11-06 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20191106_1959'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sms_log',
            old_name='nickname',
            new_name='name',
        ),
    ]
