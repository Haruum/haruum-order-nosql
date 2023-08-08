from order.models import LaundryOrder
from ..models import Review


def review_for_order_exists(laundry_order: LaundryOrder):
    return Review.objects.filter(laundry_order_id=laundry_order.get_id()).exists()


