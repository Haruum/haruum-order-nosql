from ..dto.LaundryProgressStatus import LaundryProgressStatus


class LaundryProgressStatusSerializer:
    def __init__(self, progress_status_dto, many=False):
        if many:
            self.data = []
            for status in progress_status_dto:
                self.data.append(LaundryProgressStatusSerializer._serialize(status))

        else:
            self.data = LaundryProgressStatusSerializer._serialize(progress_status_dto)

    @staticmethod
    def _serialize(progress_status_dto: LaundryProgressStatus):
        return progress_status_dto.get_all()
