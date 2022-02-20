from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Company
from .forms import CompanyForm
from django.http import HttpResponseRedirect
from datetime import datetime

def company_info(request):
    company = Company.objects.all()[0]
    context = {"company": company}
    return render(request, "company/company_info.html", context)