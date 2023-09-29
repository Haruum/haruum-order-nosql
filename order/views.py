from django.views.decorators.http import require_POST, require_GET
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers.LaundryOrderSerializer import LaundryOrderSerializer
from .serializers.LaundryOrderOutletEmailSerializer import LaundryOrderOutletEmailSerializer
from .serializers.PaymentMethodSerializer import PaymentMethodSerializer
from .services import order, payment_method

import json


@require_POST
@api_view(['POST'])
def serve_create_order(request):
    """
    This view serves as the endpoint to create
    an order.
    ---------------------------------------------
    request data must contain:
    customer_email: string
    assigned_outlet_email: string
    pickup_delivery_address: string
    payment_method_id: UUID string
    ordered_items: list

    ordered_items follows the following format
    [
        category_id: UUID string (from outlet service)
        quantity: integer
    ]
    """
    request_data = json.loads(request.body.decode('utf-8'))
    order.create_order(request_data)
    response_data = {'message': 'Order is successfully registered'}
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_get_laundry_orders_of_outlet(request):
    """
    This view returns a list of laundry orders
    assigned to an outlet specified by the email
    parameter.
    ---------------------------------------------
    request param must contain:
    email: string
    """
    request_data = request.GET
    laundry_orders = order.get_laundry_orders_of_outlet(request_data)
    response_data = LaundryOrderSerializer(laundry_orders, many=True).data
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_get_laundry_order_outlet_email(request):
    """
    This view returns the outlet email of the corresponding
    laundry order ID given in the request parameter.
    ---------------------------------------------
    request param must contain:
    laundry_order_id: UUID string
    """
    request_data = request.GET
    laundry_order = order.get_laundry_order(request_data)
    response_data = LaundryOrderOutletEmailSerializer(laundry_order).data
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_get_laundry_order_details(request):
    """
    This view serves as the endpoint to return the
    details of a laundry order specified by the
    laundry_order_id attribute
    ---------------------------------------------
    request param must contain:
    laundry_order_id: UUID string
    """
    request_data = request.GET
    laundry_order = order.get_laundry_order(request_data)
    response_data = LaundryOrderSerializer(laundry_order).data
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_get_active_laundry_orders_of_a_customer(request):
    """
    This view serves as the endpoint to return the list of
    active orders belonging to a customer.
    ---------------------------------------------
    request param must contain:
    email: string
    """
    request_data = request.GET
    active_laundry_orders = order.get_active_laundry_orders_of_customer(request_data)
    response_data = LaundryOrderSerializer(active_laundry_orders, many=True).data
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_get_completed_laundry_orders_of_a_customer(request):
    """
    This view serves as the endpoint to return the list of
    completed orders belonging to a customer.
    ---------------------------------------------
    request param must contain:
    email: string
    """
    request_data = request.GET
    completed_laundry_orders = order.get_completed_laundry_orders_of_customer(request_data)
    response_data = LaundryOrderSerializer(completed_laundry_orders, many=True).data
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_get_all_payment_methods(request):
    payment_methods = payment_method.handle_get_all_payment_method()
    response_data = PaymentMethodSerializer(payment_methods, many=True).data
    return Response(data=response_data)
