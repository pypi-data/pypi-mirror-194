from enum import Enum


class NotificationNotificationConfigTimesToRunItem(str, Enum):
    AM = "AM"
    PM = "PM"

    def __str__(self) -> str:
        return str(self.value)
