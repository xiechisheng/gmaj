# Generated by Django 2.1.7 on 2019-11-02 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20191102_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info_enterprise',
            name='dept',
        ),
    ]
