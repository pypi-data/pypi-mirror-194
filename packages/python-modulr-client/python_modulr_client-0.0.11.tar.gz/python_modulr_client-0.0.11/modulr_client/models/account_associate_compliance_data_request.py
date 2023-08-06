from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AccountAssociateComplianceDataRequest")


@attr.s(auto_attribs=True)
class AccountAssociateComplianceDataRequest:
    """Optional for associates of type C_INTEREST and an EU customer legal entity. Not to be set for other associate types
    and/or for UK customer legal entity.

        Attributes:
            relationship (str):
    """

    relationship: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        relationship = self.relationship

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "relationship": relationship,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        relationship = d.pop("relationship")

        account_associate_compliance_data_request = cls(
            relationship=relationship,
        )

        account_associate_compliance_data_request.additional_properties = d
        return account_associate_compliance_data_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
