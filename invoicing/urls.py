from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_customer', views.add_new_customer, name='new_customer'),
    path('customers', views.all_customers, name='all_customers'),
    path('customer_profile/<int:customer_id>', views.customer_profile, name='customer_profile'),
    path('<int:customer_id>/new_invoice', views.new_invoice, name='new_invoice'),
    path('<int:customer_id>/invoice/<int:invoice_id>', views.process_invoice, name='process_invoice'),
    path('delete/<int:customer_id>', views.delete_customer, name='delete_customer'),
    path('delete_invoice/<int:invoice_id>', views.delete_invoice, name='delete_invoice'),
    path('generate_pdf/<int:invoice_id>', views.generate_pdf, name='generate_pdf'),
    path('all_invioces', views.all_invoices, name='all_invoices'),
    path('delete_line/<int:line_id>', views.delete_line, name='delete_line'),
    path('scrape', views.scrape, name='scrape'),
    path('scraped/<str:name>', views.scraped, name='scraped'),
    path('toggle_paid/<int:invoice_id>', views.toggle_paid, name='toggle_paid')
]

