from enum import Enum


class AccountCustomerLegalEntity(str, Enum):
    GB = "GB"
    IE = "IE"
    NL = "NL"

    def __str__(self) -> str:
        return str(self.value)
