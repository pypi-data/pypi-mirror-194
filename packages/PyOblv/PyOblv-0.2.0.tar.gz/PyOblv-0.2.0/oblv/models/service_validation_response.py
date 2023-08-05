import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.validated_service import ValidatedService
from ..types import UNSET, Unset

T = TypeVar("T", bound="ServiceValidationResponse")


@attr.s(auto_attribs=True, repr=False)
class ServiceValidationResponse:
    """
    Attributes:
        message (Union[Unset, str]):  Default: ''.
        service (Union[Unset, ValidatedService]):
    """

    message: Union[Unset, str] = ""
    service: Union[Unset, ValidatedService] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        service: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.service, Unset):
            service = self.service.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if service is not UNSET:
            field_dict["service"] = service

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message", UNSET)

        _service = d.pop("service", UNSET)
        service: Union[Unset, ValidatedService]
        if isinstance(_service, Unset):
            service = UNSET
        else:
            service = ValidatedService.from_dict(_service)

        service_validation_response = cls(
            message=message,
            service=service,
        )

        service_validation_response.additional_properties = d
        return service_validation_response

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
