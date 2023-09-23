from datetime import datetime
import uuid


class LaundryOrder:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.date_created = datetime.utcnow()

        self.pickup_delivery_address = None
        self.owning_customer_email = None
        self.assigned_outlet_email = None

        self.status_id = None
        self.payment_method_id = None

        self.transaction_amount = 0
        self.laundry_receipts = []
        self.review = None

    def set_values_from_request(self, request_data):
        self.owning_customer_email = request_data.get('customer_email')
        self.assigned_outlet_email = request_data.get('assigned_outlet_email')
        self.pickup_delivery_address = request_data.get('pickup_delivery_address')
        self.payment_method_id = request_data.get('payment_method_id')

    def set_values_from_result(self, result):
        self.id = result.get('id')
        self.date_created = result.get('date_created')
        self.transaction_amount = result.get('transaction_amount')
        self.pickup_delivery_address = result.get('pickup_delivery_address')
        self.owning_customer_email = result.get('owning_customer_email')
        self.assigned_outlet_email = result.get('assigned_outlet_email')
        self.status_id = result.get('status_id')
        self.payment_method_id = result.get('payment_method_id')
        self.laundry_receipts = result.get('laundry_receipts')
        self.review = result.get('review')

    def set_laundry_receipts(self, laundry_receipts):
        self.laundry_receipts = laundry_receipts

    def set_status_id(self, status_id):
        self.status_id = status_id

    def set_review(self, review):
        self.review = review

    def get_id(self):
        return self.id

    def get_date_created(self):
        return self.date_created

    def get_transaction_amount(self):
        return self.transaction_amount

    def get_pickup_delivery_address(self):
        return self.pickup_delivery_address

    def get_owning_customer_email(self):
        return self.owning_customer_email

    def get_assigned_outlet_email(self):
        return self.assigned_outlet_email

    def get_status_id(self):
        return self.status_id

    def get_payment_method_id(self):
        return self.payment_method_id

    def get_laundry_receipts(self):
        return self.laundry_receipts

    def get_laundry_items_count(self):
        return sum([laundry_receipt.get('quantity') for laundry_receipt in self.laundry_receipts])

    def get_review(self):
        return self.review

    def has_been_reviewed(self):
        return self.review is not None

    def get_all(self):
        return {
            'id': self.get_id(),
            'date_created': self.get_date_created(),
            'transaction_amount': self.get_transaction_amount(),
            'pickup_delivery_address': self.get_pickup_delivery_address(),
            'owning_customer_email': self.get_owning_customer_email(),
            'assigned_outlet_email': self.get_assigned_outlet_email(),
            'status_id': self.get_status_id(),
            'payment_method_id': self.get_payment_method_id(),
            'laundry_receipts': self.get_laundry_receipts(),
            'review': self.get_review(),
        }

