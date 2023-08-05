from enum import Enum


class AccountAssociateResponseType(str, Enum):
    BENE_OWNER = "BENE_OWNER"
    CSECRETARY = "CSECRETARY"
    C_INTEREST = "C_INTEREST"
    DIRECTOR = "DIRECTOR"
    INDIVIDUAL = "INDIVIDUAL"
    PARTNER = "PARTNER"
    PCM_INDIVIDUAL = "PCM_INDIVIDUAL"
    SIGNATORY = "SIGNATORY"
    SOLETRADER = "SOLETRADER"
    TRUST_BENEFICIARY = "TRUST_BENEFICIARY"
    TRUST_SETTLOR = "TRUST_SETTLOR"
    TRUST_TRUSTEE = "TRUST_TRUSTEE"

    def __str__(self) -> str:
        return str(self.value)
