from enum import Enum


class AccountCreateCustomerRequestLegalEntity(str, Enum):
    GB = "GB"
    IE = "IE"
    NL = "NL"

    def __str__(self) -> str:
        return str(self.value)
