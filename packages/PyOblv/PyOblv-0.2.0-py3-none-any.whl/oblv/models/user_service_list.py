import json
from typing import Any, Dict, List, Type, TypeVar

import attr

from .user_services import UserServices
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserServiceList")


@attr.s(auto_attribs=True, repr=False)
class UserServiceList:
    """
    Attributes:
        total_pages (int):
        services (List[UserServices]):
    """

    total_pages: int
    services: List[UserServices]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_pages = self.total_pages
        services = []
        for services_item_data in self.services:
            services_item = services_item_data.to_dict()

            services.append(services_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_pages": total_pages,
                "services": services,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_pages = d.pop("total_pages")

        services = []
        _services = d.pop("services")
        for services_item_data in _services:
            services_item = UserServices.from_dict(services_item_data)

            services.append(services_item)

        user_services_list = cls(
            total_pages=total_pages,
            services=services,
        )

        user_services_list.additional_properties = d
        return user_services_list

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

    def __str__(self):
        return json.dumps(self.to_dict(), indent=2)

    def __repr__(self):
        return str(self)
