"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from xml.etree import ElementTree
from cloudcafe.blockstorage.volumes_api.common.models.automarshalling import \
    _VolumesAPIBaseListModel, _VolumesAPIBaseModel, _XMLDictionary


class VolumeResponse(_VolumesAPIBaseModel):
    obj_model_key = 'volume'
    kwarg_map = {
        "id_": "id",
        "display_name": "display_name",
        "size": "size",
        "volume_type": "volume_type",
        "display_description": "display_description",
        "metadata": "metadata",
        "availability_zone": "availability_zone",
        "snapshot_id": "snapshot_id",
        "attachments": "attachments",
        "created_at": "created_at",
        "links": "links",
        "status": "status"}

    def __init__(
            self, id_=None, display_name=None, size=None, volume_type=None,
            display_description=None, metadata=None, availability_zone=None,
            snapshot_id=None, attachments=None, created_at=None, status=None,
            links=None):

        self.id_ = id_
        self.display_name = display_name
        self.display_description = display_description
        self.size = size
        self.volume_type = volume_type
        self.availability_zone = availability_zone
        self.snapshot_id = snapshot_id
        self.created_at = created_at
        self.status = status
        self.links = links or []
        self.attachments = attachments or []
        self.metadata = metadata or {}

    @classmethod
    def _json_to_obj(cls, serialized_str):
        volume = super(VolumeResponse, cls)._json_to_obj(serialized_str)
        volume.attachments = _VolumeAttachmentsList._json_dict_to_obj(
            volume.attachments)
        volume.links = _LinksList._json_dict_to_obj(volume.links)
        return volume

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        kwargs = {}
        for local_kw, deserialized_obj_kw in cls.kwarg_map.iteritems():
            kwargs[local_kw] = element.get(deserialized_obj_kw)

        volume = cls(**kwargs)
        volume.metadata = _XMLDictionary._xml_ele_to_obj(element)
        volume.attachments = _VolumeAttachmentsList._xml_ele_to_obj(element)
        volume.links = _LinksList._xml_ele_to_obj(element)
        return volume


class VolumeSnapshotResponse(_VolumesAPIBaseModel):
    obj_model_key = 'snapshot'
    kwarg_map = {
        "id_": "id",
        "volume_id": "volume_id",
        "display_name": "display_name",
        "display_description": "display_description",
        "status": "status",
        "size": "size",
        "created_at": "created_at",
        "metadata": "metadata"}

    def __init__(
            self, id_=None, volume_id=None, display_name=None,
            display_description=None, status=None, size=None, created_at=None,
            metadata=None):

        self.id_ = id_
        self.volume_id = volume_id
        self.display_name = display_name
        self.display_description = display_description
        self.status = status
        self.size = size
        self.created_at = created_at
        self.metadata = metadata or {}

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        kwargs = {}
        for local_kw, deserialized_obj_kw in cls.kwarg_map.iteritems():
            kwargs[local_kw] = element.get(deserialized_obj_kw)

        snapshot = cls(**kwargs)
        snapshot.metadata = _XMLDictionary._xml_ele_to_obj(element)
        return snapshot


class VolumeTypeResponse(_VolumesAPIBaseModel):
    obj_model_key = "volume_type"
    kwarg_map = {
        "id_": "id",
        "name": "name",
        "extra_specs": "extra_specs"}

    def __init__(self, id_=None, name=None, extra_specs=None):

        self.id_ = id_
        self.name = name
        self.extra_specs = extra_specs or {}

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        kwargs = {}
        for local_kw, deserialized_obj_kw in cls.kwarg_map.iteritems():
            kwargs[local_kw] = element.get(deserialized_obj_kw)
        volume_type_obj = cls(**kwargs)
        volume_type_obj.extra_specs = _XMLDictionary._xml_ele_to_obj(
            element, 'extra_specs')
        return volume_type_obj


class VolumeListResponse(_VolumesAPIBaseListModel):
    list_model_key = 'volumes'
    ObjectModel = VolumeResponse


class VolumeSnapshotListResponse(_VolumesAPIBaseListModel):
    list_model_key = 'snapshots'
    ObjectModel = VolumeSnapshotResponse


class VolumeTypeListResponse(_VolumesAPIBaseListModel):
    list_model_key = 'volume_types'
    ObjectModel = VolumeTypeResponse


class _VolumeAttachmentItem(_VolumesAPIBaseModel):
    kwarg_map = {
        "id_": "id",
        "device": "device",
        "volume_id": "volume_id",
        "server_id": "server_id"}

    def __init__(self, id_=None, device=None, server_id=None, volume_id=None):
        self.id_ = id_
        self.device = device
        self.volume_id = volume_id
        self.server_id = server_id


class _VolumeAttachmentsList(_VolumesAPIBaseListModel):
    list_model_key = 'attachments'
    ObjectModel = _VolumeAttachmentItem

    @classmethod
    def _json_to_obj(cls, serialized_str):
        raise NotImplementedError

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplementedError


class _LinksItem(_VolumesAPIBaseModel):
    kwarg_map = {
        "href": "href",
        "rel": "rel"}

    def __init__(self, href=None, rel=None):
        self.href = href
        self.rel = rel


class _LinksList(_VolumesAPIBaseListModel):
    list_model_key = 'links'
    ObjectModel = _LinksItem
