from django.core.exceptions import ObjectDoesNotExist
from haruum_order.settings import DATABASE
from haruum_order.collections import PAYMENT_METHOD
from ..dto.PaymentMethod import PaymentMethod


def get_payment_method_by_id(payment_method_id):
    found_method = DATABASE[PAYMENT_METHOD].find_one({'id': payment_method_id})

    if found_method is not None:
        payment_method = PaymentMethod()
        payment_method.set_values_from_result(found_method)
        return payment_method

    else:
        raise ObjectDoesNotExist(f'Payment method with {payment_method_id} does not exist')


def payment_method_with_id_exists(payment_method_id):
    try:
        get_payment_method_by_id(payment_method_id)
        return True

    except ObjectDoesNotExist:
        return False


def get_all_payment_methods():
    raw_payment_methods = DATABASE[PAYMENT_METHOD].find({})

    transformed_payment_methods = []
    for raw_payment_method in raw_payment_methods:
        payment_method = PaymentMethod()
        payment_method.set_values_from_result(raw_payment_method)
        transformed_payment_methods.append(payment_method)

    return transformed_payment_methods



