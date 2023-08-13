from django.core.exceptions import ObjectDoesNotExist
from haruum_order import utils as haruum_order_utils
from haruum_order.decorators import catch_exception_and_convert_to_invalid_request_decorator
from haruum_order.exceptions import InvalidRequestException, FailedToFetchException
from haruum_order.settings import OUTLET_ORDER_COMPLETION_URL
from order.models import LaundryProgressStatus, LaundryOrder
from order.services import utils as order_utils
from . import utils


STATUS_TRANSITION_MESSAGE = 'Order with status {} can only be updated to {}'


def get_laundry_progress_status():
    return LaundryProgressStatus.objects.all()


def validate_progress_status_update(request_data):
    if not haruum_order_utils.is_valid_uuid_string(request_data.get('laundry_order_id')):
        raise InvalidRequestException('Laundry Order ID must be a valid UUID string')

    if not haruum_order_utils.is_valid_uuid_string(request_data.get('status_id')):
        raise InvalidRequestException('Status ID must be a valid UUID string')

    if not utils.laundry_progress_status_exists(request_data.get('status_id')):
        raise InvalidRequestException(f'Status with ID {request_data.get("status_id")} does not exist')


def validate_status_transition(laundry_order: LaundryOrder, new_status: LaundryProgressStatus):
    current_status = utils.get_laundry_progress_status_by_id(str(laundry_order.get_status_id()))

    if current_status.get_name() == 'pending' and new_status.get_name() != 'received':
        raise InvalidRequestException(STATUS_TRANSITION_MESSAGE.format('pending', 'received'))

    if current_status.get_name() == 'received' and new_status.get_name() != 'washed':
        raise InvalidRequestException(STATUS_TRANSITION_MESSAGE.format('received', 'washed'))

    if current_status.get_name() == 'washed' and new_status.get_name() != 'dried':
        raise InvalidRequestException(STATUS_TRANSITION_MESSAGE.format('washed', 'dried'))

    if current_status.get_name() == 'dried' and new_status.get_name() != 'returned':
        raise InvalidRequestException(STATUS_TRANSITION_MESSAGE.format('dried', 'returned'))

    if current_status.get_name() == 'returned':
        raise InvalidRequestException('Returned order can no longer be updated')


def register_laundry_progress_new_status(laundry_order: LaundryOrder, progress_status: LaundryProgressStatus):
    laundry_order.set_status_id(progress_status.id)


def decrease_outlet_workload(laundry_order: LaundryOrder, progress_status: LaundryProgressStatus):
    if progress_status.get_name() == 'returned':
        outlet_data = {'laundry_outlet_email': laundry_order.get_outlet_email()}
        haruum_order_utils.request_post_and_return_response(outlet_data, OUTLET_ORDER_COMPLETION_URL)


@catch_exception_and_convert_to_invalid_request_decorator((ObjectDoesNotExist,))
def update_laundry_progress_status(request_data):
    validate_progress_status_update(request_data)
    new_progress_status = utils.get_laundry_progress_status_by_id(request_data.get('status_id'))
    laundry_order = order_utils.get_laundry_order_from_id_thread_safe(request_data.get('laundry_order_id'))
    validate_status_transition(laundry_order, new_progress_status)
    register_laundry_progress_new_status(laundry_order, new_progress_status)
    decrease_outlet_workload(laundry_order, new_progress_status)



