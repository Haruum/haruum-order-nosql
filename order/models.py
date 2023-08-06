from django.db import models
import uuid


class LaundryOrder(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        auto_created=True,
        editable=False,
    )

    date_created = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.FloatField()
    delivery_address = models.TextField()
    owning_customer_email = models.EmailField()
    assigned_outlet_email = models.EmailField()
    status_id = models.UUIDField(default=uuid.uuid4)
    payment_method_id = models.UUIDField(default=uuid.uuid4)


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










