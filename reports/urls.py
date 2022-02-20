from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('', views.index, name='index'),
    path('new_report/<int:customer_id>', views.new_report, name='new_report'),
    path('edit_report/<int:report_id>', views.edit_report, name='edit_report'),
    path('delete_report/<int:report_id>', views.delete_report, name='delete_report'),
    ]