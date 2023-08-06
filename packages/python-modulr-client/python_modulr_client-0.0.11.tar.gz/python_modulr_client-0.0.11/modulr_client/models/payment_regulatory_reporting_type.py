from enum import Enum


class PaymentRegulatoryReportingType(str, Enum):
    BOTH = "BOTH"
    CRED = "CRED"
    DEBT = "DEBT"

    def __str__(self) -> str:
        return str(self.value)
