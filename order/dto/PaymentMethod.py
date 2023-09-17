class PaymentMethod:
    def __init__(self):
        self.id = None
        self.name = None

    def set_values_from_result(self, result):
        self.id = result.get('id')
        self.name = result.get('name')

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
