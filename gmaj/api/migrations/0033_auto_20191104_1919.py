# Generated by Django 2.1.7 on 2019-11-04 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_info_check_checker_info_check_log'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info_check_log',
            old_name='endtime',
            new_name='end_time',
        ),
    ]
