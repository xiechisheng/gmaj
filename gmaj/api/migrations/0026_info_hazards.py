# Generated by Django 2.1.7 on 2019-11-02 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20191101_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='info_hazards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('region', models.CharField(max_length=128)),
                ('contact', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=16)),
                ('type', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('level', models.CharField(max_length=16)),
            ],
        ),
    ]
