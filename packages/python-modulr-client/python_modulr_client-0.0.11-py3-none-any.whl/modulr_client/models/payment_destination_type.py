from enum import Enum


class PaymentDestinationType(str, Enum):
    ACCOUNT = "ACCOUNT"
    BENEFICIARY = "BENEFICIARY"
    IBAN = "IBAN"
    SCAN = "SCAN"

    def __str__(self) -> str:
        return str(self.value)
