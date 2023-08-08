from django.core.exceptions import ObjectDoesNotExist
from ..models import (
    PaymentMethod,
    LaundryProgressStatus,
    LaundryOrder,
)
import uuid


def payment_method_of_id_exists(payment_method_id: str) -> bool:
    return PaymentMethod.objects.filter(id=uuid.UUID(payment_method_id)).exists()


def get_progress_status_from_name(status_name: str) -> LaundryProgressStatus:
    return LaundryProgressStatus.objects.filter(name=status_name).first()


def get_laundry_order_from_id(laundry_order_id: str) -> LaundryOrder:
    try:
        return LaundryOrder.objects.get(id=uuid.UUID(laundry_order_id))

    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f'Laundry order with ID {laundry_order_id} does not exist')


def get_laundry_order_from_id_thread_safe(laundry_order_id: str):
    found_order = LaundryOrder.objects.filter(id=uuid.UUID(laundry_order_id)).select_for_update()

    if len(found_order) > 0:
        return found_order[0]

    else:
        raise ObjectDoesNotExist(f'Laundry order with ID {laundry_order_id} does not exist')
