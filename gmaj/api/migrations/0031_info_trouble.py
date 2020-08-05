# Generated by Django 2.1.7 on 2019-11-04 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_info_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='info_trouble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64)),
                ('source', models.CharField(max_length=32)),
                ('type', models.CharField(max_length=16)),
                ('describe', models.CharField(max_length=128)),
                ('level', models.CharField(max_length=16)),
                ('status', models.CharField(max_length=16)),
                ('dept', models.CharField(max_length=32)),
                ('enterprise', models.CharField(max_length=64)),
                ('reporter', models.CharField(max_length=32)),
                ('time', models.DateTimeField()),
            ],
        ),
    ]