from django.forms import ModelForm
from django import forms
from .models import Customer, Phone, Invoice, Line

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

class LineForm(ModelForm):
    vat_included = forms.CheckboxInput()

    class Meta:
        model = Line
        fields = ['item', 'amount', 'price', 'vat_included']

class SearchCompany(forms.Form):
    search_string = forms.CharField()

class DueTime(forms.Form):
    due_time = forms.IntegerField()

