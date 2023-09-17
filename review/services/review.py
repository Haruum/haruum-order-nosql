from django.core.exceptions import ObjectDoesNotExist
from haruum_order import utils as haruum_order_utils
from haruum_order.decorators import catch_exception_and_convert_to_invalid_request_decorator
from haruum_order.exceptions import InvalidRequestException
from haruum_order.settings import OUTLET_RATING_UPDATE_URL
from order.dto.LaundryOrder import LaundryOrder
from order.repositories import order as order_repository
from status.repositories import status as status_repository


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

    if request_data.get('rating') <= 2 and not isinstance(request_data.get('comment'), str):
        raise InvalidRequestException('Comment must be a string')


def validate_review_can_be_added_for_order(laundry_order: LaundryOrder):
    """
    1. Validate laundry order type is returned
    2. Validate review for order does not exist
    """
    returned_progress_status = status_repository.get_status_by_name('returned')

    if laundry_order.get_status_id() != returned_progress_status.get_id():
        raise InvalidRequestException('Review cannot be added as order has not been completed ')

    if laundry_order.has_been_reviewed():
        raise InvalidRequestException('A review for laundry order has been submitted')


def register_review_for_order(laundry_order: LaundryOrder, review_data: dict, database_session):
    order_repository.update_order_review(
        laundry_order.get_id(),
        {
            'rating': review_data.get('rating'),
            'comment': review_data.get('comment'),
        },
        database_session=database_session
    )


def update_outlet_rating(outlet_email, rating):
    """
    Send request to update outlet rating in outlet service
    """
    rating_data = {'laundry_outlet_email': outlet_email, 'new_rating': rating}
    haruum_order_utils.request_post_and_return_response(rating_data, OUTLET_RATING_UPDATE_URL)


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def create_review_for_order(request_data: dict, database_session):
    validate_review_for_order(request_data)
    laundry_order = order_repository.get_order_by_id(request_data.get('laundry_order_id'))
    validate_review_can_be_added_for_order(laundry_order)
    register_review_for_order(laundry_order, request_data, database_session=database_session)
    update_outlet_rating(laundry_order.get_assigned_outlet_email(), request_data.get('rating'))


def get_reviews_of_outlet(request_data: dict):
    orders_of_outlet = order_repository.get_orders_of_outlet(request_data.get('email'))

    reviews_for_orders = []
    for order in orders_of_outlet:
        review = order.get_review()

        if review is not None:
            review['order_id'] = order.get_id()
            reviews_for_orders.append(review)

    return reviews_for_orders



