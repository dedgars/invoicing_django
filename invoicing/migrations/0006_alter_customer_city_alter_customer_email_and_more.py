# Generated by Django 4.0.2 on 2022-02-13 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0005_line_vat_included_alter_line_amount_alter_line_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='notes',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='customer',
            name='registration',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='vat',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]