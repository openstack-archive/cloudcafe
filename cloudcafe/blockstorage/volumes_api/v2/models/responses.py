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

from cloudcafe.blockstorage.volumes_api.common.models.automarshalling import \
    _VolumesAPIBaseListModel, _VolumesAPIBaseModel, _XMLDictionary
from cloudcafe.blockstorage.volumes_api.common.models.automarshalling import \
    CommonModelProperties

# Import common responses
from cloudcafe.blockstorage.volumes_api.common.models.responses import \
    QuotaUsageResponse, QuotaListResponse, QuotaSet


class VolumeResponse(CommonModelProperties, _VolumesAPIBaseModel):
    obj_model_key = 'volume'
    kwarg_map = {
        "id_": "id",
        "size": "size",
        "volume_type": "volume_type",
        "name": "name",
        "description": "description",
        "metadata": "metadata",
        "bootable": "bootable",
        "availability_zone": "availability_zone",
        "snapshot_id": "snapshot_id",
        "attachments": "attachments",
        "links": "links",
        "created_at": "created_at",
        "status": "status",
        "source_volid": "source_volid",
        "image_ref": "imageRef",
        "volume_image_metadata": "volume_image_metadata",
        "os_vol_host_attr_host": "os-vol-host-attr:host",
        "os_vol_tenant_attr_tenant_id": "os-vol-tenant-attr:tenant_id",
        "os_vol_mig_status_attr_migstat": "os-vol-mig-status-attr:migstat",
        "os_vol_mig_status_attr_name_id": "os-vol-mig-status-attr:name_id"}

    def __init__(
            self, id_=None, size=None, name=None, volume_type=None,
            description=None, metadata=None, availability_zone=None,
            snapshot_id=None, attachments=None, created_at=None, status=None,
            links=None, source_volid=None, os_vol_tenant_attr_tenant_id=None,
            os_vol_host_attr_host=None, bootable=None, image_ref=None,
            volume_image_metadata=None, os_vol_mig_status_attr_migstat=None,
            os_vol_mig_status_attr_name_id=None):

        super(VolumeResponse, self).__init__()
        self._name = None
        self._description = None
        self.id_ = id_
        self.size = size
        self.name = name
        self.description = description
        self.volume_type = volume_type
        self.availability_zone = availability_zone
        self.metadata = metadata or {}
        self.snapshot_id = snapshot_id
        self.bootable = bootable
        self.attachments = attachments or []
        self.created_at = created_at
        self.status = status
        self.links = links or []
        self.image_ref = image_ref
        self.source_volid = source_volid
        self.volume_image_metadata = volume_image_metadata
        self.os_vol_host_attr_host = os_vol_host_attr_host
        self.os_vol_tenant_attr_tenant_id = os_vol_tenant_attr_tenant_id
        self.os_vol_mig_status_attr_migstat = os_vol_mig_status_attr_migstat
        self.os_vol_mig_status_attr_name_id = os_vol_mig_status_attr_name_id

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        volume = cls._map_values_to_kwargs(json_dict)
        volume.attachments = _VolumeAttachmentsList._json_dict_to_obj(
            volume.attachments)
        volume.links = _LinksList._json_dict_to_obj(volume.links)
        return volume

    @classmethod
    def _xml_ele_to_obj(cls, element):
        kwargs = {}
        for local_kw, deserialized_obj_kw in cls.kwarg_map.iteritems():
            kwargs[local_kw] = element.get(deserialized_obj_kw)

        namespace_kwargs = {}
        namespace_kwargs["os_vol_host_attr_host"] = "host"
        namespace_kwargs["os_vol_tenant_attr_tenant_id"] = "tenant_id"
        namespace_kwargs["os_vol_mig_status_attr_migstat"] = "migstat"
        namespace_kwargs["os_vol_mig_status_attr_name_id"] = "name_id"

        for local_kw, expected_stripped_name in namespace_kwargs.iteritems():
            for element_name, element_value in element.items():
                _, _, stripped_element_name = str(element_name).rpartition('}')
                if expected_stripped_name == stripped_element_name:
                    kwargs[local_kw] = element_value

        volume = cls(**kwargs)
        volume.metadata = _XMLDictionary._xml_ele_to_obj(element)
        volume.volume_image_metadata = _XMLDictionary._xml_ele_to_obj(
            element, 'volume_image_metadata')
        volume.attachments = _VolumeAttachmentsList._xml_ele_to_obj(element)
        volume.links = _LinksList._xml_ele_to_obj(element)
        return volume


class VolumeSnapshotResponse(CommonModelProperties, _VolumesAPIBaseModel):
    obj_model_key = 'snapshot'
    kwarg_map = {
        "id_": "id",
        "volume_id": "volume_id",
        "name": "name",
        "description": "description",
        "status": "status",
        "size": "size",
        "created_at": "created_at",
        "metadata": "metadata",
        "os_extended_snapshot_attributes_project_id":
        "os-extended-snapshot-attributes:project_id",
        "os_extended_snapshot_attributes_progress":
        "os-extended-snapshot-attributes:progress"}

    def __init__(
            self, id_=None, volume_id=None, name=None, description=None,
            status=None, size=None, created_at=None, metadata=None,
            os_extended_snapshot_attributes_project_id=None,
            os_extended_snapshot_attributes_progress=None):

        super(VolumeSnapshotResponse, self).__init__()
        self._name = None
        self._description = None
        self.id_ = id_
        self.volume_id = volume_id
        self.name = name
        self.description = description
        self.status = status
        self.size = size
        self.created_at = created_at
        self.metadata = metadata
        self.os_extended_snapshot_attributes_project_id = \
            os_extended_snapshot_attributes_project_id
        self.os_extended_snapshot_attributes_progress = \
            os_extended_snapshot_attributes_progress

    @classmethod
    def _xml_ele_to_obj(cls, element):
        kwargs = {}
        for local_kw, deserialized_obj_kw in cls.kwarg_map.iteritems():
            kwargs[local_kw] = element.get(deserialized_obj_kw)

        namespace_kwargs = {}
        namespace_kwargs[
            "os_extended_snapshot_attributes_project_id"] = "project_id"
        namespace_kwargs[
            "os_extended_snapshot_attributes_progress"] = "progress"

        for local_kw, expected_stripped_name in namespace_kwargs.iteritems():
            for element_name, element_value in element.items():
                _, _, stripped_element_name = str(element_name).rpartition('}')
                if expected_stripped_name == stripped_element_name:
                    kwargs[local_kw] = element_value

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

        super(VolumeTypeResponse, self).__init__()
        self.id_ = id_
        self.name = name
        self.extra_specs = extra_specs

    @classmethod
    def _xml_ele_to_obj(cls, element):
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

    @classmethod
    def _xml_ele_to_obj(cls, xml_etree_element):
        obj_list = cls()
        for element in xml_etree_element:
            if element.tag.endswith(cls.ObjectModel.obj_model_key):
                obj_list.append(cls.ObjectModel._xml_ele_to_obj(element))
        return obj_list


class _VolumeAttachmentItem(_VolumesAPIBaseModel):
    kwarg_map = {
        "id_": "id",
        "device": "device",
        "volume_id": "volume_id",
        "server_id": "server_id"}

    def __init__(self, id_=None, device=None, server_id=None, volume_id=None):
        super(_VolumeAttachmentItem, self).__init__()
        self.id_ = id_
        self.device = device
        self.volume_id = volume_id
        self.server_id = server_id


class _VolumeAttachmentsList(_VolumesAPIBaseListModel):
    list_model_key = 'attachments'
    ObjectModel = _VolumeAttachmentItem


class _LinksItem(_VolumesAPIBaseModel):
    kwarg_map = {
        "href": "href",
        "rel": "rel"}

    def __init__(self, href=None, rel=None):
        super(_LinksItem, self).__init__()
        self.href = href
        self.rel = rel


class _LinksList(_VolumesAPIBaseListModel):
    list_model_key = 'links'
    ObjectModel = _LinksItem
