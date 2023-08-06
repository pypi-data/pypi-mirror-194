from enum import Enum


class InboundpaymentInboundPaymentRequestType(str, Enum):
    INT_INTERC = "INT_INTERC"
    PI_BACS = "PI_BACS"
    PI_CHAPS = "PI_CHAPS"
    PI_DD = "PI_DD"
    PI_FAST = "PI_FAST"
    PI_FP = "PI_FP"
    PI_SECT = "PI_SECT"
    PI_SEPA_INST = "PI_SEPA_INST"
    PO_REV = "PO_REV"

    def __str__(self) -> str:
        return str(self.value)
