from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ReportForm
from .models import Report
from invoicing.models import Customer
from django.utils import timezone


def index(request):

    return render(request, "reports/index.html")

def new_report(request, customer_id):
    # read document number
    try:
        with open('count.txt') as count_file:
            content = count_file.read()
            count = int(content)
    except Exception:
        count = 1

    customer = Customer.objects.get(pk=customer_id)
    form = ReportForm(initial={
        'name': customer.name,
        'address': customer.address,
        'phone': customer.phone,
        'email': customer.email,
        'date_time': timezone.now().strftime('%d.%m.%Y'),
        'number': f"{datetime.today().strftime('%d%m%y')}-{count}"
    })

    context = {"form": form, "customer": customer}

    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.instance.customer = customer
            form.save()
            # increment number for the next document
            with open('count.txt', 'w') as count_file:
                count_file.write(str(count + 1))
            return redirect('customer_profile', customer_id=customer.id)

    return render(request, 'reports/new_report.html', context)


def edit_report(request, report_id):
    obj = Report.objects.get(pk=report_id)
    if request.method == "GET":
        form = ReportForm(instance=obj)
    else:
        form = ReportForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'reports/edit_report.html', {"form": form})

def delete_report(request, report_id):
    Report.objects.get(pk=report_id).delete()
    return redirect(request.META.get('HTTP_REFERER'))



