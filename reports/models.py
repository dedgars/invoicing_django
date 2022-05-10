from django.db import models
from django.utils import timezone


class Report(models.Model):
    objects = models.Manager()

    customer = models.ForeignKey("invoicing.Customer",
                                 on_delete=models.CASCADE,
                                 verbose_name="customer",
                                 related_name="reports",
                                 default=1)
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.CharField(max_length=100, blank=True)
    date_time = models.CharField(max_length=20, blank=True)
    number = models.CharField(max_length=20, blank=True)
    boiler = models.CharField(max_length=200, blank=True)
    comission = models.CharField(max_length=20, blank=True)
    gas_type = models.CharField(max_length=50, blank=True)
    thermostat = models.CharField(max_length=200, blank=True)
    maintenance = models.BooleanField(default=False)
    repairs = models.BooleanField(default=False)
    repairs_info = models.CharField(max_length=500, blank=True)
    inspection = models.BooleanField(default=False)
    flue_gas_type = models.CharField(max_length=20, blank=True)
    flue_gas_check = models.BooleanField(default=False)
    air_check = models.BooleanField(default=False)
    safety_systems_check = models.BooleanField(default=False)
    gas_conn_check = models.BooleanField(default=False)
    gas_water_tightness_check = models.BooleanField(default=False)
    system_hydr_check = models.BooleanField(default=False)
    anode_check = models.CharField(max_length=20, blank=True)
    heat_carrier = models.CharField(max_length=200, blank=True)
    yes_check = models.BooleanField(default=False)
    maintenance_need_check = models.BooleanField(default=False)
    repairs_need_check = models.BooleanField(default=False)
    notes = models.CharField(max_length=500, blank=True)
    date_created = models.DateTimeField(default=timezone.now())
