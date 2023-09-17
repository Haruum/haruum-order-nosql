class LaundryOrderReceipt:
    def __init__(self):
        self.item_category_provided_id = None
        self.item_price = None
        self.quantity = None

    def set_values_from_request(self, request_data):
        self.item_category_provided_id = request_data.get('category_id')
        self.quantity = request_data.get('quantity')

    def set_item_price(self, item_price):
        self.item_price = item_price

    def get_category_id(self):
        return self.item_category_provided_id

    def get_quantity(self):
        return self.quantity

    def get_subtotal(self):
        return self.item_price * self.quantity

    def get_all(self):
        return {
            'item_category_provided_id': self.get_category_id(),
            'quantity': self.get_quantity(),
            'subtotal': self.get_subtotal()
        }
