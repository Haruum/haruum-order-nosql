from django.db import transaction
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
    return Response(data='Hello')



