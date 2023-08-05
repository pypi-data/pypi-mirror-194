from enum import Enum


class PispgatewayDestinationType(str, Enum):
    ACCOUNT = "ACCOUNT"
    SCAN = "SCAN"

    def __str__(self) -> str:
        return str(self.value)
