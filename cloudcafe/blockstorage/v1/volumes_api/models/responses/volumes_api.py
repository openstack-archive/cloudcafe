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


class _VolumesAPIBaseModel(AutoMarshallingModel):
    obj_model_key = None
    kwarg_map = {}

    @classmethod
    def _map_values_to_kwargs(cls, deserialized_obj):
        kwargs = {}
        for local_kw, deserialized_obj_kw in cls.kwarg_map.iteritems():
            kwargs[local_kw] = deserialized_obj.get(deserialized_obj_kw)

        return cls(**kwargs)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        volume_dict = json_dict.get(cls.obj_model_key)
        return cls._json_dict_to_obj(volume_dict)

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        return cls._map_values_to_kwargs(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        return cls._map_values_to_kwargs(element)


class _VolumesAPIBaseListModel(AutoMarshallingListModel):
    list_model_key = None
    ObjectModel = None

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        dict_list = json_dict.get(cls.list_model_key)
        return cls._json_dict_to_obj(dict_list)

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        obj_list = cls()
        for obj_dict in json_dict:
            obj_list.append(cls.ObjectModel._json_dict_to_obj(obj_dict))
        return obj_list

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        list_element = ElementTree.fromstring(serialized_str)
        return cls._xml_ele_to_obj(list_element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_etree_element):
        obj_list = cls()
        for obj_element in xml_etree_element:
            obj_list.append(cls.ObjectModel._xml_ele_to_obj(obj_element))
        return obj_list


class Volume(_VolumesAPIBaseModel):
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
        "status": "status"}

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


class VolumeSnapshot(_VolumesAPIBaseModel):
    obj_model_key = 'snapshot'
    kwarg_map = {
        "id_": "id",
        "volume_id": "volume_id",
        "display_name": "display_name",
        "display_description": "display_description",
        "status": "status",
        "size": "size",
        "created_at": "created_at",
        "name": "name"}

    def __init__(
            self, id_=None, volume_id=None, display_name=None,
            display_description=None, status=None, size=None, created_at=None,
            name=None):

        self.id_ = id_
        self.volume_id = volume_id
        self.display_name = display_name
        self.display_description = display_description
        self.status = status
        self.size = size
        self.created_at = created_at
        self.name = name


class VolumeType(_VolumesAPIBaseModel):
    obj_model_key = "volume_type"
    kwarg_map = {
        "id_": "id",
        "name": "name",
        "extra_specs": "extra_specs"}

    def __init__(self, id_=None, name=None, extra_specs=None):

        self.id_ = id_
        self.name = name
        self.extra_specs = extra_specs


class VolumeList(_VolumesAPIBaseListModel):
    list_model_key = 'volumes'
    ObjectModel = Volume


class VolumeSnapshotList(_VolumesAPIBaseListModel):
    list_model_key = 'snapshots'
    ObjectModel = VolumeSnapshot


class VolumeTypeList(_VolumesAPIBaseListModel):
    list_model_key = 'volume_types'
    ObjectModel = VolumeType
