from django.contrib import admin
from .models import Customer, Invoice, Line, Phone

# Register your models here.
admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(Line)
admin.site.register(Phone)
