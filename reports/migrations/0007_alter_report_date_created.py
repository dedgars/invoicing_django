# Generated by Django 4.0.2 on 2022-04-17 06:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_alter_report_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 17, 6, 29, 35, 30467, tzinfo=utc)),
        ),
    ]
