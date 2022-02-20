from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Customer, Invoice, Line
from .forms import CustomerForm, LineForm, SearchCompany, DueTime
from django.http import HttpResponseRedirect
from datetime import datetime
from .scrape_company import get_company, get_company_data
from reports.models import Report

VAT = 1.21


def index(request):
    context = {
        "invoices": Invoice.objects.all().order_by('-id')[:5],
        "reports": Report.objects.all().order_by('-id')[:5]
    }

    return render(request, "invoicing/index.html", context)


def add_new_customer(request):
    form = CustomerForm()
    customers = Customer.objects.all()
    context = {
        "form": form,
        "customers": customers
    }
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            currentcustomer = form.save()
            return redirect('customer_profile', customer_id=currentcustomer.id)
            # return redirect('all_customers')
        else:
            print("not valid form")
    return render(request, "invoicing/new_customer.html", context)


def all_customers(request):
    context = {"customers": Customer.objects.all()}
    return render(request, "invoicing/customers.html", context)


def customer_profile(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)

    context = {
        "customer": customer,
        "invoices": customer.invoices.all(),
        "reports": customer.reports.all(),
    }
    return render(request, "invoicing/customer_profile.html", context)


def delete_customer(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    customer.delete()
    return redirect('all_customers')


def new_invoice(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)

    invoice = Invoice(number=6, create_date=datetime.now(), customer=customer)
    invoice.save()

    try:
        with open('invoice_number.txt') as count_file:
            content = count_file.read()
            count = int(content)
    except Exception:
        count = 1

    invoice.number = f"{datetime.today().strftime('%d%m%y')}-{count}"

    # increment number for the next document
    with open('invoice_number.txt', 'w') as count_file:
        count_file.write(str(count + 1))

    invoice.save()
    return redirect('process_invoice', customer_id=customer.id, invoice_id=invoice.id)


def process_invoice(request, customer_id, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    lines = Line.objects.filter(invoice=invoice)
    form = LineForm()
    due_form = DueTime(initial={'due_time': 5})

    # item names from database for autocomplete (datalist)
    previous_items = set([line.item for line in Line.objects.all()])

    customer = Customer.objects.get(pk=customer_id)
    context = {"invoice": invoice,
               "form": form,
               "lines": lines,
               "customer": customer,
               "items": previous_items,  # datalist items
               "due_form": due_form,
               }

    if request.method == "POST":
        if 'add-line' in request.POST:
            form = LineForm(request.POST)
            if form.is_valid():
                item = form.cleaned_data["item"]
                amount = form.cleaned_data["amount"]
                price = form.cleaned_data["price"]
                vat_included = form.cleaned_data["vat_included"]
                line = Line(invoice=invoice, item=item, amount=amount, price=price, vat_included=vat_included)
                if line.vat_included:
                    line.price /= VAT
                line.save()
                return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and "save-invoice" in request.POST:
        due_form = DueTime(request.POST)

        if due_form.is_valid():
            invoice.due_time = due_form.cleaned_data["due_time"]
            invoice.save()
            return redirect('customer_profile', customer_id=customer.id)
        else:
            print("not valid form")

    return render(request, "invoicing/new_invoice.html", context)


def delete_invoice(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    customer = invoice.customer
    invoice.delete()
    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('customer_profile', customer_id=customer.id)


def generate_pdf(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    Invoice.generate_pdf(invoice)
    return redirect(request.META.get('HTTP_REFERER'))


def all_invoices(request):
    context = {"invoices": Invoice.objects.all()}
    return render(request, "invoicing/all_invoices.html", context)


def toggle_paid(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    if invoice.paid:
        invoice.paid = False
    else:
        invoice.paid = True
    invoice.save()
    return redirect(request.META.get('HTTP_REFERER'))


def delete_line(request, line_id):
    line = Line.objects.get(pk=line_id)
    line.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def scrape(request):
    form = SearchCompany()
    companies = []
    if request.method == "POST":
        form = SearchCompany(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data["search_string"]
            companies = get_company_data(search_string)
    context = {"form": form, "companies": companies}
    return render(request, "invoicing/scrape.html", context)


def scraped(request, name):
    all_companies = Customer.objects.all()
    company = get_company(get_company_data(name)[0])
    if company['vat'][0] != 'L':
        company['vat'] = None
    form = CustomerForm(initial={'name': company['name'],
                                 'registration': company['registration'],
                                 'vat': company['vat'],
                                 'address': company['address']})
    context = {
        "company": company,
        "form": form,
        "all_companies": all_companies,
    }

    return render(request, "invoicing/scraped.html", context)
