# Generated by Django 2.1.7 on 2019-11-06 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20191106_1955'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sms_log',
            old_name='name',
            new_name='name_name',
        ),
        migrations.RenameField(
            model_name='sms_log',
            old_name='user',
            new_name='user_id',
        ),
    ]