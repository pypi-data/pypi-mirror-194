from enum import Enum


class CardsimulatorCardAuthorisationResponseStatus(str, Enum):
    APPROVED = "APPROVED"
    REVERSED = "REVERSED"
    SETTLED = "SETTLED"

    def __str__(self) -> str:
        return str(self.value)
