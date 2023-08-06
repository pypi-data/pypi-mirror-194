from enum import Enum


class DirectdebitCollectionType(str, Enum):
    COLLECTION = "COLLECTION"
    INDEMNITY = "INDEMNITY"

    def __str__(self) -> str:
        return str(self.value)
