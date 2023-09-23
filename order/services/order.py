from django.core.exceptions import ObjectDoesNotExist
from haruum_order import utils as haruum_order_utils
from haruum_order.decorators import catch_exception_and_convert_to_invalid_request_decorator
from haruum_order.exceptions import FailedToFetchException, InvalidRequestException
from haruum_order.settings import (
    OUTLET_SERVICE_CATEGORIES_URL,
    OUTLET_ORDER_REGISTRATION_URL,
    OUTLET_GET_DATA_URL,
    CUSTOMER_CHECK_EXISTENCE_URL,
)
from rest_framework import status
from typing import List
from ..dto.LaundryOrder import LaundryOrder
from ..dto.LaundryOrderReceipt import LaundryOrderReceipt
from ..repositories import (
    payment as payment_repository,
    order as order_repository
)
from status.repositories import status as status_repository
import requests


def get_service_categories_of_outlet(outlet_email: str) -> List:
    """
    Fetch the service categories provided by an outlet
    """
    service_categories_url = f'{OUTLET_SERVICE_CATEGORIES_URL}{outlet_email}'

    try:
        service_categories_response = requests.get(service_categories_url)
        service_categories_result = service_categories_response.json()

        if service_categories_response.status_code != status.HTTP_200_OK:
            raise FailedToFetchException(
                f'Unexpected response with message {service_categories_result.get("message")}'
            )

        return service_categories_result

    except requests.exceptions.RequestException:
        raise FailedToFetchException('Failed to fetch outlet services')


def find_matching_category(category_id, outlet_service_categories):
    matching_category = [category for category in outlet_service_categories if category.get('id') == category_id]

    if len(matching_category) > 0:
        return matching_category[0]

    else:
        return None


def validate_single_ordered_item(order_item_datum: dict, outlet_service_categories: List[dict]):
    if find_matching_category(order_item_datum.get('category_id'), outlet_service_categories) is None:
        raise InvalidRequestException(f'Category ID {order_item_datum.get("category_id")} does not exist')

    if not isinstance(order_item_datum.get('quantity'), int):
        raise InvalidRequestException('Quantity must be an integer')


def validate_ordered_items(order_item_data, outlet_service_categories):
    """
    1. Validate category_id exists
    2. Validate quantity is an integer
    """
    for order_item_datum in order_item_data:
        validate_single_ordered_item(order_item_datum, outlet_service_categories)


def validate_customer_existence(customer_email: str):
    validation_url = f'{CUSTOMER_CHECK_EXISTENCE_URL}{customer_email}'

    try:
        customer_exists_response = requests.get(validation_url)
        validation_result = customer_exists_response.json()

        if customer_exists_response.status_code != status.HTTP_200_OK:
            raise FailedToFetchException(validation_result.get('message'))

        if not validation_result.get('customer_exists'):
            raise InvalidRequestException(f'Customer with email {customer_email} does not exist')

    except requests.exceptions.RequestException:
        raise FailedToFetchException('Failed to validate customer existence')


def get_outlet_data(outlet_email: str):
    outlet_data_url = f'{OUTLET_GET_DATA_URL}{outlet_email}'

    try:
        outlet_data_response = requests.get(outlet_data_url)
        outlet_data = outlet_data_response.json()

        if outlet_data_response.status_code == status.HTTP_400_BAD_REQUEST:
            raise InvalidRequestException(outlet_data.get('message'))

        if outlet_data_response.status_code != status.HTTP_200_OK:
            raise FailedToFetchException(outlet_data.get('message'))

        return outlet_data

    except requests.exceptions.RequestException:
        raise FailedToFetchException('Failed to validate outlet existence')


def validate_order_creation_data(request_data: dict):
    if not isinstance(request_data.get('pickup_delivery_address'), str):
        raise InvalidRequestException('Pickup/Delivery address must be a string')

    if not haruum_order_utils.is_valid_uuid_string(request_data.get('payment_method_id')):
        raise InvalidRequestException('Payment method ID must be a valid UUID string')

    if not payment_repository.payment_method_with_id_exists(request_data.get('payment_method_id')):
        raise InvalidRequestException('Payment method with id does not exist')

    if not isinstance(request_data.get('ordered_items'), list):
        raise InvalidRequestException('Ordered items must be a list')

    if len(request_data.get('ordered_items')) == 0:
        raise InvalidRequestException('Ordered items must not be empty')


def convert_ordered_items(ordered_items: list):
    converted_ordered_items = []
    for item in ordered_items:
        receipt = LaundryOrderReceipt()
        receipt.set_values_from_request(item)
        converted_ordered_items.append(receipt)

    return converted_ordered_items


def get_category_price(category_id: str, outlet_service_categories: list):
    return find_matching_category(category_id, outlet_service_categories).get('item_price')


def generate_price_for_items(ordered_items: List[LaundryOrderReceipt], outlet_service_categories: list):
    for ordered_item in ordered_items:
        category_price = get_category_price(ordered_item.get_category_id(), outlet_service_categories)
        ordered_item.set_item_price(category_price)


def generate_laundry_order_from_request(request_data: dict, converted_ordered_items: List[LaundryOrderReceipt]):
    serialized_ordered_items = [
        converted_ordered_item.get_all()
        for converted_ordered_item in converted_ordered_items
    ]

    laundry_order = LaundryOrder()
    laundry_order.set_values_from_request(request_data)
    laundry_order.set_laundry_receipts(serialized_ordered_items)

    pending_status = status_repository.get_status_by_name('pending')
    laundry_order.set_status_id(pending_status.get_id())
    return laundry_order


def register_order(laundry_order: LaundryOrder):
    try:
        order_repository.create_order(laundry_order)
        increase_outlet_workload(
            laundry_order.get_assigned_outlet_email(),
            laundry_order.get_laundry_items_count()
        )

    except Exception as exception:
        order_repository.delete_order(laundry_order.get_id())
        raise exception


def increase_outlet_workload(outlet_email: str, order_quantity: int):
    """
    Send request to increase outlet workload
    """
    outlet_data = {'laundry_outlet_email': outlet_email, 'order_quantity': order_quantity}
    haruum_order_utils.request_post_and_return_response(outlet_data, OUTLET_ORDER_REGISTRATION_URL)


def create_order(request_data: dict):
    validate_order_creation_data(request_data)
    validate_customer_existence(request_data.get('customer_email'))
    outlet_data = get_outlet_data(request_data.get('assigned_outlet_email'))
    outlet_service_categories = outlet_data.get('items_provided')
    validate_ordered_items(request_data.get('ordered_items'), outlet_service_categories)
    ordered_items = convert_ordered_items(request_data.get('ordered_items'))
    generate_price_for_items(ordered_items, outlet_service_categories)
    laundry_order = generate_laundry_order_from_request(request_data, ordered_items)
    register_order(laundry_order)


def get_laundry_orders_of_outlet(request_data: dict):
    return order_repository.get_orders_of_outlet(request_data.get('email'))


def validate_get_laundry_order_outlet_request(request_data):
    if not haruum_order_utils.is_valid_uuid_string(request_data.get('laundry_order_id')):
        raise InvalidRequestException('Laundry Order ID must be a valid UUID string')


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def get_laundry_order(request_data):
    validate_get_laundry_order_outlet_request(request_data)
    return order_repository.get_order_by_id(request_data.get('laundry_order_id'))


def get_active_laundry_orders_of_customer(request_data: dict):
    returned_progress_status = status_repository.get_status_by_name('returned')
    active_customer_orders = order_repository.get_active_laundry_orders_of_a_customer(
        request_data.get('email'),
        returned_progress_status.get_id()
    )

    return active_customer_orders


def get_completed_laundry_orders_of_customer(request_data: dict):
    returned_progress_status = status_repository.get_status_by_name('returned')
    completed_customer_orders = order_repository.get_completed_laundry_orders_of_a_customer(
        request_data.get('email'),
        returned_progress_status.get_id()
    )

    return completed_customer_orders
