from django.views.decorators.http import require_POST, require_GET
from haruum_order.decorators import transaction_atomic
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import review
import json


@require_POST
@api_view(['POST'])
@transaction_atomic()
def serve_create_review_for_order(database_session, request):
    """
    This view registers a review for a laundry order.
    ---------------------------------------------
    request data must contain:
    laundry_order_id: UUID string
    rating: integer
    comment: string
    """
    request_data = json.loads(request.body.decode('utf-8'))
    review.create_review_for_order(request_data, database_session=database_session)
    response_data = {'message': 'Review for order is created successfully'}
    return Response(data=response_data)


@require_GET
@api_view(['GET'])
def serve_get_reviews_of_outlet(request):
    """
    This view returns the list of reviews for a
    laundry outlet.
    ---------------------------------------------
    request param must contain:
    email
    """
    request_data = request.GET
    response_data = review.get_reviews_of_outlet(request_data)
    return Response(data=response_data)



