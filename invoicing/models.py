from django.db import models
from num2words import num2words
from datetime import datetime, timedelta


VAT = 1.21

class Customer(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200, blank=True)
    registration = models.CharField(max_length=20, blank=True)
    vat = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.CharField(max_length=100, blank=True)
    notes = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return f'{self.name} {self.address}'


class Invoice(models.Model):
    objects = models.Manager()
    number = models.CharField(max_length=20)
    create_date = models.DateTimeField('date created')
    due_time = models.IntegerField(default=5)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices', default=1)
    paid = models.BooleanField(default=False)

    from .pdf_gen import generate_pdf

    def __str__(self):
        return f'{self.number}'

    def due_date(self):
        date = self.create_date + timedelta(days=self.due_time)
        return date.strftime('%d.%m.%Y.')

    def total(self):
        return sum([line.amount * line.price for line in self.lines.all()])

    def vat(self):
        return self.total() * VAT - self.total()

    def total_with_vat(self):
        return self.total() * VAT

    def num_to_words(self):
        euros = num2words(int(self.total_with_vat() // 1), lang='lv')
        cents = round((self.total_with_vat() - self.total_with_vat() // 1) * 100)
        return f"Summa vārdos: {euros} eiro, {cents} centi"

class Line(models.Model):
    objects = models.Manager()
    item = models.CharField(max_length=200)
    amount = models.FloatField(default=1)
    vat_included = models.BooleanField(default=False, )
    price = models.FloatField(default=0)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='lines', default=1)

    def total(self):
        return self.amount * self.price

    def __str__(self):
        return f'{self.item} - {self.amount} - {self.price}'

class Phone(models.Model):
    num = models.CharField(max_length=200)

    def __str__(self):
        return f"Phone: {self.num}"


