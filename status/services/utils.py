from django.core.exceptions import ObjectDoesNotExist
from order.models import LaundryProgressStatus
import uuid


def laundry_progress_status_exists(status_id):
    return LaundryProgressStatus.objects.filter(id=uuid.UUID(status_id)).exists()


def get_laundry_progress_status_by_id(status_id):
    try:
        return LaundryProgressStatus.objects.get(id=uuid.UUID(status_id))

    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f'Status with id {status_id} does not exist')
