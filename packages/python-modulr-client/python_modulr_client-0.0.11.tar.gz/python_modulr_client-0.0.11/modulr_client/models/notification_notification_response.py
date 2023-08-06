from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.notification_notification_response_channel import (
    NotificationNotificationResponseChannel,
)
from ..models.notification_notification_response_status import (
    NotificationNotificationResponseStatus,
)
from ..models.notification_notification_response_type import (
    NotificationNotificationResponseType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.notification_notification_config import NotificationNotificationConfig


T = TypeVar("T", bound="NotificationNotificationResponse")


@attr.s(auto_attribs=True)
class NotificationNotificationResponse:
    """
    Attributes:
        channel (NotificationNotificationResponseChannel): Channel used to send the notification.
        config (NotificationNotificationConfig): Configuration information for this Notification entity.
        destinations (List[str]): A list of emails or url(webhook) used to send the notification. For 'EMAIL' channel
            this can be a list of comma separated email addresses. For 'WEBHOOK' channel this will be a single URL.
        id (str): Unique Identifier for the notification.
        status (NotificationNotificationResponseStatus): Status of notification.
        type (NotificationNotificationResponseType): Type of notification
        customer_id (Union[Unset, str]): Unique Identifier for the customer of this notification.
    """

    channel: NotificationNotificationResponseChannel
    config: "NotificationNotificationConfig"
    destinations: List[str]
    id: str
    status: NotificationNotificationResponseStatus
    type: NotificationNotificationResponseType
    customer_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel = self.channel.value

        config = self.config.to_dict()

        destinations = self.destinations

        id = self.id
        status = self.status.value

        type = self.type.value

        customer_id = self.customer_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel": channel,
                "config": config,
                "destinations": destinations,
                "id": id,
                "status": status,
                "type": type,
            }
        )
        if customer_id is not UNSET:
            field_dict["customerId"] = customer_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.notification_notification_config import (
            NotificationNotificationConfig,
        )

        d = src_dict.copy()
        channel = NotificationNotificationResponseChannel(d.pop("channel"))

        config = NotificationNotificationConfig.from_dict(d.pop("config"))

        destinations = cast(List[str], d.pop("destinations"))

        id = d.pop("id")

        status = NotificationNotificationResponseStatus(d.pop("status"))

        type = NotificationNotificationResponseType(d.pop("type"))

        customer_id = d.pop("customerId", UNSET)

        notification_notification_response = cls(
            channel=channel,
            config=config,
            destinations=destinations,
            id=id,
            status=status,
            type=type,
            customer_id=customer_id,
        )

        notification_notification_response.additional_properties = d
        return notification_notification_response

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
