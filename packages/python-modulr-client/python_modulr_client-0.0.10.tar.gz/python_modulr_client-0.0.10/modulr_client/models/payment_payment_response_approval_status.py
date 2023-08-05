from enum import Enum


class PaymentPaymentResponseApprovalStatus(str, Enum):
    APPROVED = "APPROVED"
    DELETED = "DELETED"
    NOTNEEDED = "NOTNEEDED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"

    def __str__(self) -> str:
        return str(self.value)
