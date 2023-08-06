import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_ import Filter
    from ..models.view_configuration import ViewConfiguration
    from ..models.view_tags import ViewTags


T = TypeVar("T", bound="View")


@attr.s(auto_attribs=True)
class View:
    """
    Attributes:
        name (str):
        filter_ (Filter):
        layout (Any):
        configuration (List['ViewConfiguration']):
        index (int):
        organization_id (Union[Unset, str]):
        url (Union[Unset, None, str]):
        is_url_authorized (Union[Unset, bool]):
        show_on_single_device (Union[Unset, bool]):
        show_on_multi_device (Union[Unset, bool]):
        show_on_teleop (Union[Unset, bool]):
        show_on_analytics (Union[Unset, bool]):
        show_timeline (Union[Unset, bool]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        tags (Union[Unset, ViewTags]):
    """

    name: str
    filter_: "Filter"
    layout: Any
    configuration: List["ViewConfiguration"]
    index: int
    organization_id: Union[Unset, str] = UNSET
    url: Union[Unset, None, str] = UNSET
    is_url_authorized: Union[Unset, bool] = UNSET
    show_on_single_device: Union[Unset, bool] = UNSET
    show_on_multi_device: Union[Unset, bool] = UNSET
    show_on_teleop: Union[Unset, bool] = UNSET
    show_on_analytics: Union[Unset, bool] = UNSET
    show_timeline: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, "ViewTags"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        filter_ = self.filter_.to_dict()

        layout = self.layout
        configuration = []
        for configuration_item_data in self.configuration:
            configuration_item = configuration_item_data.to_dict()

            configuration.append(configuration_item)

        index = self.index
        organization_id = self.organization_id
        url = self.url
        is_url_authorized = self.is_url_authorized
        show_on_single_device = self.show_on_single_device
        show_on_multi_device = self.show_on_multi_device
        show_on_teleop = self.show_on_teleop
        show_on_analytics = self.show_on_analytics
        show_timeline = self.show_timeline
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "filter": filter_,
                "layout": layout,
                "configuration": configuration,
                "index": index,
            }
        )
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if url is not UNSET:
            field_dict["url"] = url
        if is_url_authorized is not UNSET:
            field_dict["isUrlAuthorized"] = is_url_authorized
        if show_on_single_device is not UNSET:
            field_dict["showOnSingleDevice"] = show_on_single_device
        if show_on_multi_device is not UNSET:
            field_dict["showOnMultiDevice"] = show_on_multi_device
        if show_on_teleop is not UNSET:
            field_dict["showOnTeleop"] = show_on_teleop
        if show_on_analytics is not UNSET:
            field_dict["showOnAnalytics"] = show_on_analytics
        if show_timeline is not UNSET:
            field_dict["showTimeline"] = show_timeline
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.filter_ import Filter
        from ..models.view_configuration import ViewConfiguration
        from ..models.view_tags import ViewTags

        d = src_dict.copy()
        name = d.pop("name")

        filter_ = Filter.from_dict(d.pop("filter"))

        layout = d.pop("layout")

        configuration = []
        _configuration = d.pop("configuration")
        for configuration_item_data in _configuration:
            configuration_item = ViewConfiguration.from_dict(configuration_item_data)

            configuration.append(configuration_item)

        index = d.pop("index")

        organization_id = d.pop("organizationId", UNSET)

        url = d.pop("url", UNSET)

        is_url_authorized = d.pop("isUrlAuthorized", UNSET)

        show_on_single_device = d.pop("showOnSingleDevice", UNSET)

        show_on_multi_device = d.pop("showOnMultiDevice", UNSET)

        show_on_teleop = d.pop("showOnTeleop", UNSET)

        show_on_analytics = d.pop("showOnAnalytics", UNSET)

        show_timeline = d.pop("showTimeline", UNSET)

        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, ViewTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = ViewTags.from_dict(_tags)

        view = cls(
            name=name,
            filter_=filter_,
            layout=layout,
            configuration=configuration,
            index=index,
            organization_id=organization_id,
            url=url,
            is_url_authorized=is_url_authorized,
            show_on_single_device=show_on_single_device,
            show_on_multi_device=show_on_multi_device,
            show_on_teleop=show_on_teleop,
            show_on_analytics=show_on_analytics,
            show_timeline=show_timeline,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags,
        )

        view.additional_properties = d
        return view

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
