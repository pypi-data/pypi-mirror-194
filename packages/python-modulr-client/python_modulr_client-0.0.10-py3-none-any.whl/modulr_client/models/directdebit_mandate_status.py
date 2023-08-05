from enum import Enum


class DirectdebitMandateStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"
    SUSPENDED = "SUSPENDED"

    def __str__(self) -> str:
        return str(self.value)
