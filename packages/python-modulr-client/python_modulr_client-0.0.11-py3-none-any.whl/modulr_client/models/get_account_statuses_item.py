from enum import Enum


class GetAccountStatusesItem(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    CLIENT_BLOCKED = "CLIENT_BLOCKED"
    CLOSED = "CLOSED"

    def __str__(self) -> str:
        return str(self.value)
