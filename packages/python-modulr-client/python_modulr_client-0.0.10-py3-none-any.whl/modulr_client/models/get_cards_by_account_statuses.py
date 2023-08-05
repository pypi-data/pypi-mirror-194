from enum import Enum


class GetCardsByAccountStatuses(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"
    CREATED = "CREATED"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"

    def __str__(self) -> str:
        return str(self.value)
