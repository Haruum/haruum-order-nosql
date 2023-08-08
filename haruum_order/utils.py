import uuid


def is_valid_uuid_string(uuid_string: str) -> bool:
    try:
        uuid.UUID(uuid_string)
        return True

    except (TypeError, ValueError):
        return False
