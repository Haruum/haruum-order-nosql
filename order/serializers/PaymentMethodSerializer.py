class PaymentMethodSerializer:
    def __init__(self, payment_method_dto, many=False):
        if many:
            self.data = []
            for payment_method in payment_method_dto:
                self.data.append(PaymentMethodSerializer._serialize(payment_method))

        else:
            self.data = PaymentMethodSerializer._serialize(payment_method_dto)

    @staticmethod
    def _serialize(payment_method_dto):
        return {
            'id': payment_method_dto.get_id(),
            'name': payment_method_dto.get_name()
        }