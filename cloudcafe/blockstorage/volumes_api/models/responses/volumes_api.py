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

import json
from xml.etree import ElementTree

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel


class Volume(AutoMarshallingModel):
    TAG = 'volume'
    '''@TODO Make sub data model for attachments element'''
    def __init__(
            self, id_=None, display_name=None, size=None, volume_type=None,
            display_description=None, metadata=None, availability_zone=None,
            snapshot_id=None, attachments=None, created_at=None, status=None,
            xmlns=None):

        #Common attributes
        self.id_ = id_
        self.display_name = display_name
        self.display_description = display_description
        self.size = size
        self.volume_type = volume_type
        self.metadata = metadata or {}
        self.availability_zone = availability_zone
        self.snapshot_id = snapshot_id
        self.attachments = attachments
        self.created_at = created_at
        self.status = status
        self.xmlns = xmlns

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        volume_dict = json_dict.get(cls.TAG)
        return cls._json_dict_to_obj(volume_dict)

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        return Volume(
            id_=json_dict.get('id'),
            display_name=json_dict.get('display_name'),
            size=json_dict.get('size'),
            volume_type=json_dict.get('volume_type'),
            display_description=json_dict.get('display_description'),
            metadata=json_dict.get('metadata'),
            availability_zone=json_dict.get('availability_zone'),
            snapshot_id=json_dict.get('snapshot_id'),
            attachments=json_dict.get('attachments'),
            created_at=json_dict.get('created_at'),
            status=json_dict.get('status'))

    #Response Deserializers
    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        return Volume(
            id_=element.get('id'),
            display_name=element.get('display_name'),
            size=element.get('size'),
            volume_type=element.get('volume_type'),
            display_description=element.get('display_description'),
            metadata=element.get('metadata'),
            availability_zone=element.get('availability_zone'),
            snapshot_id=element.get('snapshot_id'),
            attachments=element.get('attachments'),
            created_at=element.get('created_at'),
            status=element.get('status'))


class VolumeList(AutoMarshallingListModel):
    TAG = 'volumes'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        volume_dict_list = json_dict.get(cls.TAG)
        return cls._json_dict_to_obj(volume_dict_list)

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        volume_list = VolumeList()
        for volume_dict in json_dict:
            volume_list.append(Volume._json_dict_to_obj(volume_dict))
        return volume_list

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        volume_list_element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(volume_list_element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_etree_element):
        volume_list = VolumeList()
        for volume_element in xml_etree_element:
            volume_list.append(Volume._xml_ele_to_obj(volume_element))
        return volume_list


class VolumeSnapshot(AutoMarshallingModel):
    TAG = 'snapshot'

    def __init__(self, id_=None, volume_id=None, display_name=None,
                 display_description=None, status=None,
                 size=None, created_at=None, name=None):

        self.id_ = id_
        self.volume_id = volume_id
        self.display_name = display_name
        self.display_description = display_description
        self.status = status
        self.size = size
        self.created_at = created_at
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        volume_snap_dict = json_dict.get(cls.TAG)
        return cls._json_dict_to_obj(volume_snap_dict)

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        return VolumeSnapshot(
            id_=json_dict.get('id'),
            volume_id=json_dict.get('volume_id'),
            display_name=json_dict.get('display_name'),
            display_description=json_dict.get('display_description'),
            status=json_dict.get('status'),
            size=json_dict.get('size'),
            created_at=json_dict.get('created_at'),
            name=json_dict.get('name'))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        volume_snap_element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(volume_snap_element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_etree_element):
        return VolumeSnapshot(
            id_=xml_etree_element.get('id'),
            volume_id=xml_etree_element.get('volume_id'),
            display_name=xml_etree_element.get('display_name'),
            display_description=xml_etree_element.get('display_description'),
            status=xml_etree_element.get('status'),
            size=xml_etree_element.get('size'),
            created_at=xml_etree_element.get('created_at'),
            name=xml_etree_element.get('name'))


class VolumeSnapshotList(AutoMarshallingListModel):
    TAG = 'snapshots'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        volume_snap_dict_list = json_dict.get(cls.TAG)
        return cls._json_dict_to_obj(volume_snap_dict_list)

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        volume_snap_list = VolumeSnapshotList()
        for volume_snap_dict in json_dict:
            volume_snap_list.append(VolumeSnapshot._json_dict_to_obj(
                volume_snap_dict))
        return volume_snap_list

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        volume_snap_list_element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(volume_snap_list_element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_etree_element):
        volume_snap_list = VolumeSnapshotList()
        for volume_snap_element in xml_etree_element:
            volume_snap_list.append(VolumeSnapshot._xml_ele_to_obj(
                volume_snap_element))
        return volume_snap_list


class VolumeType(AutoMarshallingModel):
    TAG = 'volume_type'

    def __init__(self, id_=None, name=None, extra_specs=None):

        self.id_ = id_
        self.name = name
        self.extra_specs = extra_specs

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        volume_type_dict = json_dict.get(cls.TAG)
        return cls._json_dict_to_obj(volume_type_dict)

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        return VolumeType(
            id_=json_dict.get('id_'),
            name=json_dict.get('name'),
            extra_specs=json_dict.get('extra_specs'))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        volume_type_element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(volume_type_element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_etree_element):
        return VolumeType(
            id_=xml_etree_element.get('id_'),
            name=xml_etree_element.get('name'),
            extra_specs=xml_etree_element.get('extra_specs'))


class VolumeTypeList(AutoMarshallingListModel):
    TAG = 'volume_types'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        volume_type_dict_list = json_dict.get(cls.TAG)
        return cls._json_dict_to_obj(volume_type_dict_list)

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        volume_type_list = VolumeTypeList()
        for volume_type_dict in json_dict:
            volume_type_list.append(VolumeType._json_dict_to_obj(
                volume_type_dict))
        return volume_type_list

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        volume_type_list_element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(volume_type_list_element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_etree_element):
        volume_type_list = VolumeTypeList()
        for volume_type_element in xml_etree_element:
            volume_type_list.append(VolumeType._xml_ele_to_obj(
                volume_type_element))
        return volume_type_list
