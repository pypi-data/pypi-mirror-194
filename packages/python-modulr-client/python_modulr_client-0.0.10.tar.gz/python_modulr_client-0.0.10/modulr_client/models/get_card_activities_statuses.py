from enum import Enum


class GetCardActivitiesStatuses(str, Enum):
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"
    EXPIRED = "EXPIRED"
    SETTLED = "SETTLED"

    def __str__(self) -> str:
        return str(self.value)
