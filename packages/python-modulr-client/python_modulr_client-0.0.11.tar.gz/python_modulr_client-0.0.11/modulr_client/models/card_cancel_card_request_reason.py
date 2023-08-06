from enum import Enum


class CardCancelCardRequestReason(str, Enum):
    DESTROYED = "DESTROYED"
    LOST = "LOST"
    STOLEN = "STOLEN"

    def __str__(self) -> str:
        return str(self.value)
