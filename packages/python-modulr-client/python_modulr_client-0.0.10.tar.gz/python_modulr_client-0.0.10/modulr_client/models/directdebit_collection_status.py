from enum import Enum


class DirectdebitCollectionStatus(str, Enum):
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    PROCESSING = "PROCESSING"
    REPRESENTABLE = "REPRESENTABLE"
    REPRESENTED = "REPRESENTED"
    SCHEDULED = "SCHEDULED"
    SUCCESS = "SUCCESS"

    def __str__(self) -> str:
        return str(self.value)
