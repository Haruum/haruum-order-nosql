from django.core.exceptions import ObjectDoesNotExist
from haruum_order.settings import DATABASE
from haruum_order.collections import STATUS
from status.dto.LaundryProgressStatus import LaundryProgressStatus


def get_status_by_name(name: str):
    found_status_raw = DATABASE[STATUS].find_one({'name': name})

    if found_status_raw is not None:
        status = LaundryProgressStatus()
        status.set_values_from_result(found_status_raw)
        return status

    else:
        raise ObjectDoesNotExist(f'Status with name {name} does not exist')


def get_status_by_id(payment_id: str):
    found_status_raw = DATABASE[STATUS].find_one({'id': payment_id})

    if found_status_raw is not None:
        status = LaundryProgressStatus()
        status.set_values_from_result(found_status_raw)
        return status

    else:
        raise ObjectDoesNotExist(f'Status with ID {id} does not exist')


def get_all_status():
    all_statuses_raw = DATABASE[STATUS].find({})

    all_statuses = []
    for status_raw in all_statuses_raw:
        status = LaundryProgressStatus()
        status.set_values_from_result(status_raw)
        all_statuses.append(status)

    return all_statuses

