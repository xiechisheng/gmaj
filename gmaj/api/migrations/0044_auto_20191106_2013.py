# Generated by Django 2.1.7 on 2019-11-06 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20191106_2000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sms_log',
            old_name='user',
            new_name='user_id',
        ),
    ]
