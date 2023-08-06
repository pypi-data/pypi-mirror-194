from enum import Enum


class GetAccessGroupsTypesItem(str, Enum):
    DELEGATE = "DELEGATE"
    SERVICE_CUSTOMER = "SERVICE_CUSTOMER"
    SERVICE_PARTNER = "SERVICE_PARTNER"
    USER_DEFINED = "USER_DEFINED"

    def __str__(self) -> str:
        return str(self.value)
