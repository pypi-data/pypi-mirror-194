from enum import Enum


class CardCardResponseStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"
    CREATED = "CREATED"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"

    def __str__(self) -> str:
        return str(self.value)
