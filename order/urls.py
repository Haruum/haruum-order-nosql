from django.urls import path
from .views import (
    serve_create_order,
    serve_get_laundry_orders_of_outlet,
    serve_get_laundry_order_outlet_email,
    serve_get_laundry_order_details,
    serve_get_active_laundry_orders_of_a_customer,
    serve_get_completed_laundry_orders_of_a_customer,
)


urlpatterns = [
    path('create/', serve_create_order),
    path('outlet-orders/', serve_get_laundry_orders_of_outlet),
    path('customer-orders/active/', serve_get_active_laundry_orders_of_a_customer),
    path('customer-orders/completed/', serve_get_completed_laundry_orders_of_a_customer),
    path('outlet-email/', serve_get_laundry_order_outlet_email),
    path('detail/', serve_get_laundry_order_details),
]
