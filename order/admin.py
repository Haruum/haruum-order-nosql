from django.contrib import admin
from .models import (
    LaundryOrder,
    LaundryProgressStatus,
    LaundryOrderReceipt,
    PaymentMethod
)

admin.site.register(LaundryOrder)
admin.site.register(LaundryProgressStatus)
admin.site.register(LaundryOrderReceipt)
admin.site.register(PaymentMethod)



