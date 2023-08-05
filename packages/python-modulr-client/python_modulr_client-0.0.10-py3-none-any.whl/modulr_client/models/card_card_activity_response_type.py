from enum import Enum


class CardCardActivityResponseType(str, Enum):
    AUTHORISATION = "AUTHORISATION"
    REFUND = "REFUND"
    REVERSAL = "REVERSAL"
    SETTLEMENT = "SETTLEMENT"

    def __str__(self) -> str:
        return str(self.value)
