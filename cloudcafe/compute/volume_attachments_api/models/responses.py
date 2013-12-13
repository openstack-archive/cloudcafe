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


class VolumeAttachmentResponse(AutoMarshallingModel):

    def __init__(self, id_=None, volume_id=None, server_id=None, device=None):
        super(VolumeAttachmentResponse, self).__init__()
        self.id_ = id_
        self.volume_id = volume_id
        self.server_id = server_id
        self.device = device

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        data = data.get("volumeAttachment", dict())
        return cls._dict_to_obj(data)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        return cls._dict_to_obj(ElementTree.fromstring(serialized_str))

    @classmethod
    def _dict_to_obj(cls, obj_dict):
        return VolumeAttachmentResponse(
            id_=obj_dict.get('id', None),
            volume_id=obj_dict.get('volumeId', None),
            server_id=obj_dict.get('serverId', None),
            device=obj_dict.get('device', None))


class VolumeAttachmentListResponse(AutoMarshallingListModel):
    """Represents a list of VolumeAttachmentResponse objects"""

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        return cls._xml_ele_to_obj(ElementTree.fromstring(serialized_str))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        data = data.get("volumeAttachments")
        return cls._list_to_obj(data)

    @classmethod
    def _list_to_obj(cls, obj_list):
        return VolumeAttachmentListResponse(
            [VolumeAttachmentResponse._dict_to_obj(obj) for obj in obj_list])
