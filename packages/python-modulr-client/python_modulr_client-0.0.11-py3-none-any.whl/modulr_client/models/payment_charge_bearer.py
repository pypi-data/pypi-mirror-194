from enum import Enum


class PaymentChargeBearer(str, Enum):
    CRED = "CRED"
    DEBT = "DEBT"
    SHAR = "SHAR"

    def __str__(self) -> str:
        return str(self.value)
