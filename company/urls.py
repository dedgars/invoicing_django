from django.urls import path
from . import views

app_name = 'company'
urlpatterns = [
    path('', views.company_info, name='company_info'),
    ]