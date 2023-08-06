from enum import Enum


class DirectdebitCollectionScheduleResponseStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"

    def __str__(self) -> str:
        return str(self.value)
