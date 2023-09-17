from django.core.exceptions import ObjectDoesNotExist

from haruum_order.settings import DATABASE
from haruum_order.collections import ORDER
from ..dto.LaundryOrder import LaundryOrder


def create_order(order_dto: LaundryOrder):
    DATABASE[ORDER].insert_one(order_dto.get_all())
    return order_dto


def update_order_status(order_id, progress_status_id):
    DATABASE[ORDER].update_one(
        {'id': order_id},
        {'$set': {'status_id': progress_status_id}}
    )


def update_order_review(order_id, review):
    DATABASE[ORDER].update_one(
        {'id': order_id},
        {'$set': {'review': review}}
    )


def delete_order(order_id):
    DATABASE[ORDER].delete_one({'id': order_id})


def get_orders_of_outlet(outlet_email):
    matching_orders_raw = DATABASE[ORDER].find({'assigned_outlet_email': outlet_email})

    matching_orders = []
    for matching_order_raw_data in matching_orders_raw:
        matching_order = LaundryOrder()
        matching_order.set_values_from_result(matching_order_raw_data)
        matching_orders.append(matching_order)

    return matching_orders


def get_order_by_id(laundry_order_id):
    found_order_raw = DATABASE[ORDER].find_one({'id': laundry_order_id})

    if found_order_raw is not None:
        order = LaundryOrder()
        order.set_values_from_result(found_order_raw)
        return order

    else:
        raise ObjectDoesNotExist(f'Laundry order with ID {laundry_order_id} does not exist')


def get_active_laundry_orders_of_a_customer(customer_email, returned_status_id):
    matching_orders_raw = DATABASE[ORDER].find({
        'owning_customer_email': customer_email,
        'status_id': {
            '$ne': returned_status_id
        }
    })

    matching_orders = []
    for matching_order_raw_data in matching_orders_raw:
        matching_order = LaundryOrder()
        matching_order.set_values_from_result(matching_order_raw_data)
        matching_orders.append(matching_order)

    return matching_orders


def get_completed_laundry_orders_of_a_customer(customer_email, returned_status_id):
    matching_orders_raw = DATABASE[ORDER].find({
        'owning_customer_email': customer_email,
        'status_id': returned_status_id
    })

    matching_orders = []
    for matching_order_raw_data in matching_orders_raw:
        matching_order = LaundryOrder()
        matching_order.set_values_from_result(matching_order_raw_data)
        matching_orders.append(matching_order)

    return matching_orders


