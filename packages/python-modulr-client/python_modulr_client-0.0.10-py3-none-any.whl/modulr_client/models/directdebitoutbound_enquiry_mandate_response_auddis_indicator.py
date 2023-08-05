from enum import Enum


class DirectdebitoutboundEnquiryMandateResponseAuddisIndicator(str, Enum):
    A = "A"
    N = "N"

    def __str__(self) -> str:
        return str(self.value)
