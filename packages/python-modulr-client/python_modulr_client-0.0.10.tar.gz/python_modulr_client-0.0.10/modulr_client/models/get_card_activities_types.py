from enum import Enum


class GetCardActivitiesTypes(str, Enum):
    AUTHORISATION = "AUTHORISATION"
    REFUND = "REFUND"
    REVERSAL = "REVERSAL"
    SETTLEMENT = "SETTLEMENT"

    def __str__(self) -> str:
        return str(self.value)
