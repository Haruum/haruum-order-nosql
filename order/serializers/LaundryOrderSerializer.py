from ..repositories import payment as payment_repository
from status.repositories import status as status_repository


class LaundryOrderSerializer:
    def __init__(self, order_dto, many=False):
        if many:
            self.data = []
            for order in order_dto:
                self.data.append(LaundryOrderSerializer._serialize(order))

        else:
            self.data = LaundryOrderSerializer._serialize(order_dto)

    @staticmethod
    def _get_status_name_by_id(status_id):
        return status_repository.get_status_by_id(status_id).get_name()

    @staticmethod
    def _get_payment_method_name(payment_method_id):
        return payment_repository.get_payment_method_by_id(payment_method_id).get_name()

    @staticmethod
    def _serialize(order_dto):
        return {
            'id': order_dto.get_id(),
            'date_created': order_dto.get_date_created(),
            'transaction_amount': order_dto.get_transaction_amount(),
            'pickup_delivery_address': order_dto.get_pickup_delivery_address(),
            'owning_customer_email': order_dto.get_owning_customer_email(),
            'assigned_outlet_email': order_dto.get_assigned_outlet_email(),
            'status_id': order_dto.get_status_id(),
            'status_name': LaundryOrderSerializer._get_status_name_by_id(order_dto.get_status_id()),
            'payment_method_id': order_dto.get_payment_method_id(),
            'payment_method_name': LaundryOrderSerializer._get_payment_method_name(order_dto.get_payment_method_id()),
            'laundry_receipts': order_dto.get_laundry_receipts(),
            'review': order_dto.get_review(),
            'customer_name': order_dto.get_customer_name(),
            'customer_phone_number': order_dto.get_customer_phone_number(),
            'outlet_name': order_dto.get_outlet_name(),
            'outlet_phone_number': order_dto.get_outlet_phone_number(),
            'outlet_address': order_dto.get_outlet_address()
        }


