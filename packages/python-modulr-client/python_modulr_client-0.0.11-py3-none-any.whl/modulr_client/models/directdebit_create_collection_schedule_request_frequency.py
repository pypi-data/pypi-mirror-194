from enum import Enum


class DirectdebitCreateCollectionScheduleRequestFrequency(str, Enum):
    ANNUALLY = "ANNUALLY"
    EVERY_FOUR_WEEKS = "EVERY_FOUR_WEEKS"
    EVERY_TWO_WEEKS = "EVERY_TWO_WEEKS"
    MONTHLY = "MONTHLY"
    ONCE = "ONCE"
    QUARTERLY = "QUARTERLY"
    SEMI_ANNUALLY = "SEMI_ANNUALLY"
    WEEKLY = "WEEKLY"

    def __str__(self) -> str:
        return str(self.value)
