from django.db import transaction
from django.views.decorators.http import require_GET, require_POST
from order.models import LaundryProgressStatusSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import status
import json


@require_GET
@api_view(['GET'])
def serve_get_laundry_progress_statuses(request):
    """
    This view serves as the endpoint to return
    the list of progress status.
    ---------------------------------------------
    """
    progress_statuses = status.get_laundry_progress_status()
    response_data = LaundryProgressStatusSerializer(progress_statuses, many=True).data
    return Response(data=response_data)


@require_POST
@api_view(['POST'])
@transaction.atomic()
def serve_update_laundry_progress_status(request):
    """
    This method serves as the endpoint to update laundry order
    progress status.
    This method is implemented in a thread-safe manner to prevent
    false reading in the customer's side were the order be read and
    updated simultaneously.
    ---------------------------------------------
    request data must contain:
    laundry_order_id: UUID string
    status_id: UUID string
    """
    request_data = json.loads(request.body.decode('utf-8'))
    status.update_laundry_progress_status(request_data)
    response_data = {'message': 'Laundry Order status is successfully updated'}
    return Response(data=response_data)


