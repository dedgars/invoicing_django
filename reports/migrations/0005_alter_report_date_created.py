# Generated by Django 4.0.2 on 2022-04-16 11:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_report_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 16, 11, 8, 21, 971693, tzinfo=utc)),
        ),
    ]
