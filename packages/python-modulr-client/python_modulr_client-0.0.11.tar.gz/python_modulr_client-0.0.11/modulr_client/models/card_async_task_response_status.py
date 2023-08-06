from enum import Enum


class CardAsyncTaskResponseStatus(str, Enum):
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"
    RECEIVED = "RECEIVED"
    RUNNING = "RUNNING"

    def __str__(self) -> str:
        return str(self.value)
