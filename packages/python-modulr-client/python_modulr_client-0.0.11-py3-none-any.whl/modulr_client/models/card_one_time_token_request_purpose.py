from enum import Enum


class CardOneTimeTokenRequestPurpose(str, Enum):
    READ = "READ"
    UPDATE = "UPDATE"

    def __str__(self) -> str:
        return str(self.value)
