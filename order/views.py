from django.db import transaction
from django.views.decorators.http import require_POST, require_GET
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import LaundryOrderSerializer
from .services import order

import json


@require_POST
@api_view(['POST'])
@transaction.atomic()
def serve_create_order(request):
    """
    This method serves as the endpoint to create
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
    This method returns a list of laundry orders
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


