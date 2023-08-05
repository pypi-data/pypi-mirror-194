from enum import Enum


class InboundpaymentAccountIdentifierDetailRequestType(str, Enum):
    DD = "DD"
    IBAN = "IBAN"
    INTL = "INTL"
    SCAN = "SCAN"

    def __str__(self) -> str:
        return str(self.value)
