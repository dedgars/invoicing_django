# Generated by Django 4.0.2 on 2022-04-17 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0007_invoice_due_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='invoicing.customer'),
        ),
        migrations.AlterField(
            model_name='line',
            name='invoice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='invoicing.invoice'),
        ),
    ]