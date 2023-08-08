from django.db import models
from rest_framework import serializers
from review.models import Review, ReviewSerializer
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
    has_review = models.BooleanField(default=False)

    def has_been_reviewed(self):
        return self.has_review

    def review(self):
        self.has_review = True
        self.save()

    def get_id(self):
        return self.id

    def set_transaction_amount(self, transaction_amount):
        self.transaction_amount = transaction_amount
        self.save()

    def get_status_id(self):
        return self.status_id

    def set_status_id(self, status_id):
        self.status_id = status_id
        self.save()

    def get_payment_method_id(self):
        return self.payment_method_id

    def get_outlet_email(self):
        return self.assigned_outlet_email


class LaundryOrderSerializer(serializers.ModelSerializer):
    status_name = serializers.SerializerMethodField('get_status_name')
    payment_method_name = serializers.SerializerMethodField('get_payment_method_name')
    review = serializers.SerializerMethodField('get_review_of_order')

    def get_review_of_order(self, laundry_order: LaundryOrder):
        review_of_order = Review.objects.filter(laundry_order_id=laundry_order.get_id())

        if len(review_of_order) > 0:
            return ReviewSerializer(review_of_order[0]).data

        else:
            return None

    def get_status_name(self, laundry_order: LaundryOrder):
        return LaundryProgressStatus.objects.get(id=laundry_order.get_status_id()).name

    def get_payment_method_name(self, laundry_order: LaundryOrder):
        return PaymentMethod.objects.get(id=laundry_order.get_payment_method_id()).name

    class Meta:
        model = LaundryOrder
        fields = [
            'id',
            'date_created',
            'transaction_amount',
            'pickup_delivery_address',
            'owning_customer_email',
            'assigned_outlet_email',
            'status_id',
            'status_name',
            'payment_method_id',
            'payment_method_name',
            'review'
        ]


class LaundryOrderOutletEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryOrder
        fields = [
            'id',
            'assigned_outlet_email'
        ]


class LaundryProgressStatus(models.Model):
    id = models.UUIDField(
        primary_key=True,
        auto_created=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=20)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id


class LaundryProgressStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryProgressStatus
        fields = '__all__'


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










