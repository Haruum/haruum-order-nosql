from ..repositories import payment as payment_repository


def handle_get_all_payment_method():
    return payment_repository.get_all_payment_methods()
