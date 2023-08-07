from django.db import models
from rest_framework import serializers
import uuid


class LaundryOrder(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        auto_created=True,
        editable=False,
    )

    date_created = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.FloatField(null=True)
    pickup_delivery_address = models.TextField()
    owning_customer_email = models.EmailField()
    assigned_outlet_email = models.EmailField()
    status_id = models.UUIDField(default=uuid.uuid4)
    payment_method_id = models.UUIDField(default=uuid.uuid4)

    def set_transaction_amount(self, transaction_amount):
        self.transaction_amount = transaction_amount
        self.save()

    def get_status_id(self):
        return self.status_id

    def get_payment_method_id(self):
        return self.payment_method_id


class LaundryOrderSerializer(serializers.ModelSerializer):
    status_name = serializers.SerializerMethodField('get_status_name')
    payment_method_name = serializers.SerializerMethodField('get_payment_method_name')

    def get_status_name(self, laundry_order: LaundryOrder):
        return LaundryProgressStatus.objects.get(id=laundry_order.get_status_id()).name

    def get_payment_method_name(self, laundry_order: LaundryOrder):
        return PaymentMethod.objects.get(id=laundry_order.get_payment_method_id()).name

    class Meta:
        model = LaundryOrder
        fields = [
            'date_created',
            'transaction_amount',
            'pickup_delivery_address',
            'owning_customer_email',
            'assigned_outlet_email',
            'status_id',
            'status_name',
            'payment_method_id',
            'payment_method_name'
        ]


class LaundryProgressStatus(models.Model):
    id = models.UUIDField(
        primary_key=True,
        auto_created=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=20)


class PaymentMethod(models.Model):
    id = models.UUIDField(
        primary_key=True,
        auto_created=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)


class LaundryOrderReceipt(models.Model):
    id = models.UUIDField(
        primary_key=True,
        auto_created=True,
        default=uuid.uuid4,
        editable=False
    )

    quantity = models.IntegerField()
    subtotal = models.FloatField()
    item_category_provided_id = models.UUIDField()
    laundry_order_id = models.UUIDField()










