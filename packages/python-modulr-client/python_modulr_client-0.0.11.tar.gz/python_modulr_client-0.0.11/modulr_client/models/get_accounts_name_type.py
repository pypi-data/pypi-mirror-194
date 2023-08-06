from enum import Enum


class GetAccountsNameType(str, Enum):
    CONTAINS = "CONTAINS"
    EXACT = "EXACT"
    PREFIX = "PREFIX"
    SUFFIX = "SUFFIX"
    WORD_MATCH = "WORD_MATCH"
    WORD_MATCH_ALPHANUMERIC = "WORD_MATCH_ALPHANUMERIC"

    def __str__(self) -> str:
        return str(self.value)
