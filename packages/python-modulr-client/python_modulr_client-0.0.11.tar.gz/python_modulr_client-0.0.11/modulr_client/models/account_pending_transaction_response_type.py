from enum import Enum


class AccountPendingTransactionResponseType(str, Enum):
    ADHOC = "ADHOC"
    FE_ACMNT = "FE_ACMNT"
    FE_ACOPN = "FE_ACOPN"
    FE_REV = "FE_REV"
    FE_TXN = "FE_TXN"
    INT_INTERC = "INT_INTERC"
    INT_INTRAC = "INT_INTRAC"
    PI_BACS = "PI_BACS"
    PI_BACS_CONTRA = "PI_BACS_CONTRA"
    PI_CHAPS = "PI_CHAPS"
    PI_DD = "PI_DD"
    PI_FAST = "PI_FAST"
    PI_FAST_REV = "PI_FAST_REV"
    PI_MASTER = "PI_MASTER"
    PI_REV = "PI_REV"
    PI_SECT = "PI_SECT"
    PI_SEPA_INST = "PI_SEPA_INST"
    PI_SWIFT = "PI_SWIFT"
    PI_VISA = "PI_VISA"
    PO_CHAPS = "PO_CHAPS"
    PO_DD = "PO_DD"
    PO_FAST = "PO_FAST"
    PO_MASTER = "PO_MASTER"
    PO_REV = "PO_REV"
    PO_REV_MASTER = "PO_REV_MASTER"
    PO_SECT = "PO_SECT"
    PO_SEPA_INST = "PO_SEPA_INST"
    PO_SWIFT = "PO_SWIFT"
    PO_VISA = "PO_VISA"

    def __str__(self) -> str:
        return str(self.value)
