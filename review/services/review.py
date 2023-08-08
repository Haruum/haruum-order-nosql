from django.core.exceptions import ObjectDoesNotExist
from haruum_order import utils as haruum_order_utils
from haruum_order.decorators import catch_exception_and_convert_to_invalid_request_decorator
from haruum_order.exceptions import InvalidRequestException
from order.models import LaundryOrder
from order.services import utils as order_utils
from ..models import Review
from . import utils


def validate_review_for_order(request_data: dict):
    """
    1. Validate laundry_order_id is a UUID string
    2. Validate rating is an integer
    3. Validate comment exists if rating is 2 or less
    """
    if not haruum_order_utils.is_valid_uuid_string(request_data.get('laundry_order_id')):
        raise InvalidRequestException('Laundry order ID must be a valid UUID string')

    if not isinstance(request_data.get('rating'), int):
        raise InvalidRequestException('Rating must be an integer')

    if request_data.get('rating') <= 2 and not request_data.get('comment'):
        raise InvalidRequestException('Comment must exist for reviews with rating less than 3')


def validate_review_can_be_added_for_order(laundry_order: LaundryOrder):
    """
    1. Validate laundry order type is returned
    2. Validate review for order does not exist
    """
    returned_progress_status = order_utils.get_progress_status_from_name('returned')

    if laundry_order.get_status_id() != returned_progress_status.get_id():
        raise InvalidRequestException('Review cannot be added as order has not been completed ')

    if laundry_order.has_been_reviewed():
        raise InvalidRequestException('A review for laundry order has been submitted')


def register_review_for_order(laundry_order: LaundryOrder,  review_data: dict):
    laundry_order_id = review_data.get('laundry_order_id')
    rating = review_data.get('rating')
    comment = review_data.get('comment')

    Review.objects.create(
        laundry_order_id=laundry_order_id,
        rating=rating,
        comment=comment
    )
    laundry_order.review()


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def create_review_for_order(request_data: dict):
    validate_review_for_order(request_data)
    laundry_order = order_utils.get_laundry_order_from_id_thread_safe(request_data.get('laundry_order_id'))
    validate_review_can_be_added_for_order(laundry_order)
    register_review_for_order(laundry_order, request_data)


def get_reviews_of_outlet(request_data: dict):
    orders_of_outlet = LaundryOrder.objects.filter(assigned_outlet_email=request_data.get('email'))
    order_ids = list(map(lambda order: order.get_id(), orders_of_outlet))
    reviews_for_orders = Review.objects.filter(laundry_order_id__in=order_ids)
    return reviews_for_orders



