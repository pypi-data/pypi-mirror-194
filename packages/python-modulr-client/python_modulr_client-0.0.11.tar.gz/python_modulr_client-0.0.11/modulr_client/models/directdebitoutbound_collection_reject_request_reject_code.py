from enum import Enum


class DirectdebitoutboundCollectionRejectRequestRejectCode(str, Enum):
    ADVANCE_NOTICE_DISPUTED = "ADVANCE_NOTICE_DISPUTED"
    AMOUNT_DIFFERS = "AMOUNT_DIFFERS"
    AMOUNT_NOT_YET_DUE = "AMOUNT_NOT_YET_DUE"
    PRESENTATION_OVERDUE = "PRESENTATION_OVERDUE"
    SKIP_DEBIT_ATTEMPT = "SKIP_DEBIT_ATTEMPT"

    def __str__(self) -> str:
        return str(self.value)
