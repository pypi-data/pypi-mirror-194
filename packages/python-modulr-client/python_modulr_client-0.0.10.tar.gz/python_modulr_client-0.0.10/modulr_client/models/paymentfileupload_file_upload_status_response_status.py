from enum import Enum


class PaymentfileuploadFileUploadStatusResponseStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    DUPLICATE = "DUPLICATE"
    INVALID = "INVALID"
    PROCESSED = "PROCESSED"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"
    VALID = "VALID"

    def __str__(self) -> str:
        return str(self.value)
