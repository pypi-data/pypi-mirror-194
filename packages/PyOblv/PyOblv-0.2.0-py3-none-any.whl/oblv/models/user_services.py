import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserServices")


@attr.s(auto_attribs=True, repr=False)
class UserServices:
    """
    Attributes:
        repo_name (Union[Unset, str]):  Default: ''.
        repo_owner (Union[Unset, str]):  Default: ''.
        account_type (Union[Unset, str]):  Default: ''.
        ref (Union[Unset, str]):  Default: ''.
        service_validated (Union[Unset, bool]):
        sha (Union[Unset, str]):  Default: ''.
        type (Union[Unset, str]):  Default: ''.
    """

    repo_name: Union[Unset, str] = ""
    repo_owner: Union[Unset, str] = ""
    account_type: Union[Unset, str] = ""
    ref: Union[Unset, str] = ""
    service_validated: Union[Unset, bool] = False
    sha: Union[Unset, str] = ""
    type: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        repo_name = self.repo_name
        repo_owner = self.repo_owner
        account_type = self.account_type
        ref = self.ref
        service_validated = self.service_validated
        sha = self.sha
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if repo_name is not UNSET:
            field_dict["repo_name"] = repo_name
        if repo_owner is not UNSET:
            field_dict["repo_owner"] = repo_owner
        if account_type is not UNSET:
            field_dict["account_type"] = account_type
        if ref is not UNSET:
            field_dict["ref"] = ref
        if service_validated is not UNSET:
            field_dict["service_validated"] = service_validated
        if sha is not UNSET:
            field_dict["sha"] = sha
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        repo_name = d.pop("repo_name", UNSET)

        repo_owner = d.pop("repo_owner", UNSET)

        account_type = d.pop("account_type", UNSET)

        ref = d.pop("ref", UNSET)

        service_validated = d.pop("service_validated", UNSET)

        sha = d.pop("sha", UNSET)

        type = d.pop("type", UNSET)

        user_services = cls(
            repo_name=repo_name,
            repo_owner=repo_owner,
            account_type=account_type,
            ref=ref,
            service_validated=service_validated,
            sha=sha,
            type=type,
        )

        user_services.additional_properties = d
        return user_services

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
