from ..models import PaymentMethod, LaundryProgressStatus
import uuid


def payment_method_of_id_exists(payment_method_id: str) -> bool:
    return PaymentMethod.objects.filter(id=uuid.UUID(payment_method_id)).exists()


def get_progress_status_from_name(status_name: str) -> LaundryProgressStatus:
    return LaundryProgressStatus.objects.filter(name=status_name).first()