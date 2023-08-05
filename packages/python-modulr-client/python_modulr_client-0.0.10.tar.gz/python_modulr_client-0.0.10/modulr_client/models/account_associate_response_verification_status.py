from enum import Enum


class AccountAssociateResponseVerificationStatus(str, Enum):
    DECLINED = "DECLINED"
    EXVERIFIED = "EXVERIFIED"
    MIGRATED = "MIGRATED"
    REFERRED = "REFERRED"
    REVIEWED = "REVIEWED"
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"

    def __str__(self) -> str:
        return str(self.value)
