from haruum_order.settings import (
    OUTLET_SERVICE_CATEGORIES_URL,
    OUTLET_ORDER_REGISTRATION_URL,
    OUTLET_CHECK_EXISTENCE_URL,
    CUSTOMER_CHECK_EXISTENCE_URL,
)
from haruum_order.exceptions import FailedToFetchException, InvalidRequestException
from rest_framework import status
from order.services import utils
from typing import List
from ..models import LaundryOrder, LaundryOrderReceipt

import requests


def get_service_categories_of_outlet(outlet_email) -> List:
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


def validate_single_ordered_item(order_item_datum, service_categories_id):
    if item_category_id := order_item_datum.get('category_id') not in service_categories_id:
        raise InvalidRequestException(f'Category ID {item_category_id} does not exist')

    if not isinstance(order_item_datum.get('quantity'), int):
        raise InvalidRequestException('Quantity must be an integer')


def validate_ordered_items(outlet_service_categories: List[dict], order_item_data):
    """
    1. Validate category_id exists
    2. Validate quantity is an integer
    """
    service_categories_id = map(lambda service_category: service_category.get('id'), outlet_service_categories)

    for order_item_datum in order_item_data:
        validate_single_ordered_item(order_item_datum, service_categories_id)


def validate_customer_existence(customer_email):
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


def validate_outlet_existence(outlet_email):
    validation_url = f'{OUTLET_CHECK_EXISTENCE_URL}{outlet_email}'

    try:
        outlet_exists_response = requests.get(validation_url)
        validation_result = outlet_exists_response.json()

        if outlet_exists_response.status_code != status.HTTP_200_OK:
            raise FailedToFetchException(validation_result.get('message'))

        if not validation_result.get('outlet_exists'):
            raise InvalidRequestException(f'Outlet with email {outlet_email} does not exist')

    except requests.exceptions.RequestException:
        raise FailedToFetchException('Failed to validate outlet existence')


def validate_order_creation_data(request_data: dict):
    if not isinstance(request_data.get('pickup_delivery_address'), str):
        raise InvalidRequestException('Pickup/Delivery address must be a string')

    if not utils.payment_method_of_id_exists(request_data.get('payment_method_id')):
        raise InvalidRequestException('Payment method with id does not exist')

    if not isinstance(request_data.get('ordered_items'), list):
        raise InvalidRequestException('Ordered items must be a list')

    if len(request_data.get('ordered_items')) == 0:
        raise InvalidRequestException('Ordered items must not be empty')

    validate_customer_existence(request_data.get('customer_email'))
    validate_outlet_existence(request_data.get('assigned_outlet_email'))


def get_category_price(outlet_service_categories, category_id):
    return list(
        filter(
            lambda category_data: category_data.get('id') == category_id,
            outlet_service_categories
        )
    )[0].get('item_price')


def register_order(request_data, outlet_service_categories):
    pickup_delivery_address = request_data.get('pickup_delivery_address')
    owning_customer_email = request_data.get('customer_email')
    assigned_outlet_email = request_data.get('assigned_outlet_email')
    payment_method_id = request_data.get('payment_method_id')
    pending_status_id = utils.get_progress_status_from_name('pending').id

    laundry_order = LaundryOrder.objects.create(
        pickup_delivery_address=pickup_delivery_address,
        owning_customer_email=owning_customer_email,
        assigned_outlet_email=assigned_outlet_email,
        payment_method_id=payment_method_id,
        status_id=pending_status_id
    )

    ordered_items_data = request_data.get('ordered_items')
    transaction_amount = 0
    for ordered_item in ordered_items_data:
        category_id = ordered_item.get('category_id')
        quantity = ordered_item.get('quantity')
        category_price = get_category_price(outlet_service_categories, category_id)
        subtotal = quantity * category_price

        LaundryOrderReceipt.objects.create(
            quantity=quantity,
            subtotal=subtotal,
            item_category_provided_id=category_id,
            laundry_order_id=laundry_order.id
        )

        transaction_amount += subtotal

    laundry_order.set_transaction_amount(transaction_amount)


def increase_outlet_workload(outlet_email):
    """
    Send request to increase outlet workload
    """
    outlet_data = {'laundry_outlet_email': outlet_email}

    try:
        increase_outlet_response = requests.post(OUTLET_ORDER_REGISTRATION_URL, json=outlet_data)
        response_data = increase_outlet_response.json()

        if increase_outlet_response.status_code == status.HTTP_400_BAD_REQUEST:
            raise InvalidRequestException(response_data.get('message'))

        if increase_outlet_response.status_code != status.HTTP_200_OK:
            raise FailedToFetchException(response_data.get('message'))

    except requests.exceptions.RequestException:
        raise FailedToFetchException('Failed to communicate with outlet service')


def create_order(request_data: dict):
    validate_order_creation_data(request_data)
    outlet_service_categories = get_service_categories_of_outlet(request_data.get('assigned_outlet_email'))
    validate_ordered_items(outlet_service_categories, request_data.get('ordered_items'))
    register_order(request_data, outlet_service_categories)
    increase_outlet_workload(request_data.get('assigned_outlet_email'))



