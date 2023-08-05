from enum import Enum


class AccountCreateCustomerRequestType(str, Enum):
    CHARITY = "CHARITY"
    INDIVIDUAL = "INDIVIDUAL"
    LLC = "LLC"
    LLP = "LLP"
    LPARTNRSHP = "LPARTNRSHP"
    OPARTNRSHP = "OPARTNRSHP"
    PCM_BUSINESS = "PCM_BUSINESS"
    PCM_INDIVIDUAL = "PCM_INDIVIDUAL"
    PLC = "PLC"
    SOLETRADER = "SOLETRADER"
    TRUST = "TRUST"

    def __str__(self) -> str:
        return str(self.value)
