from enum import Enum


class DirectdebitoutboundMessageResponseCode(str, Enum):
    BUSINESSRULE = "BUSINESSRULE"
    CONNECTION = "CONNECTION"
    DUPLICATE = "DUPLICATE"
    GENERAL = "GENERAL"
    INVALID = "INVALID"
    MFADEVICEMM = "MFADEVICEMM"
    MFAERROR = "MFAERROR"
    MFAMESSAGEINVALID = "MFAMESSAGEINVALID"
    MFASTATUS = "MFASTATUS"
    MFATIMEOUT = "MFATIMEOUT"
    NOTFOUND = "NOTFOUND"
    PERMISSION = "PERMISSION"
    RATELIMIT = "RATELIMIT"
    RETRY = "RETRY"

    def __str__(self) -> str:
        return str(self.value)
