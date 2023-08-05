from enum import Enum


class CardCardReplacementRequestReason(str, Enum):
    DAMAGED = "DAMAGED"
    LOST = "LOST"
    RENEW = "RENEW"
    STOLEN = "STOLEN"

    def __str__(self) -> str:
        return str(self.value)
