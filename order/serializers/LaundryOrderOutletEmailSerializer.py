class LaundryOrderOutletEmailSerializer:
    def __init__(self, order_dto, many=False):
        if many:
            self.data = []
            for order in order_dto:
                self.data.append(LaundryOrderOutletEmailSerializer._serialize(order))

        else:
            self.data = LaundryOrderOutletEmailSerializer._serialize(order_dto)

    @staticmethod
    def _serialize(order_dto):
        return {
            'id': order_dto.get_id(),
            'assigned_outlet_email': order_dto.get_assigned_outlet_email(),
        }
