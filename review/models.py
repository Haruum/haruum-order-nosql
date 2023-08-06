from django.db import models
import uuid


class Review(models.Model):
    id = models.UUIDField(
        primary_key=True,
        auto_created=True,
        default=uuid.uuid4(),
        editable=True
    )

    laundry_order_id = models.UUIDField()
    rating = models.IntegerField()
    comment = models.TextField(null=True)


