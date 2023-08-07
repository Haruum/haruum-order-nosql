from django.urls import path
from .views import serve_create_order, serve_get_laundry_orders_of_outlet


urlpatterns = [
    path('create/', serve_create_order),
    path('outlet/', serve_get_laundry_orders_of_outlet),
]
