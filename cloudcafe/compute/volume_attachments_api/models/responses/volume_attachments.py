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

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel


class VolumeAttachment(AutoMarshallingModel):
    def __init__(self, id_=None, volume_id=None, server_id=None, device=None):
        self.id_ = None
        self.server_id = None
        self.volume_id = volume_id
        self.device = device

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return VolumeAttachment(
            id_=json_dict.get('id'),
            volume_id=json_dict.get('volumeId'),
            server_id=json_dict.get('serverId'),
            device=json_dict.get('device'))


class VolumeAttachmentListResponse(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''
            Handles both the single and list version of the Volume
            call, obviating the need for separate domain objects for "Volumes"
            and "Lists of Volumes" responses.
            Returns a list-like VolumeAttachmentListResponse
            of VolumeAttachment objects, even if there is only one volume
            attachment present.
        '''
        json_dict = json.loads(serialized_str)

        is_list = True if json_dict.get('volumeAttachments', None) else False

        va_list = VolumeAttachmentListResponse()
        if is_list:
            for volume_attachment in json_dict.get('volumeAttachments'):
                va = VolumeAttachment(
                    id_=volume_attachment.get('id'),
                    volume_id=volume_attachment.get('volumeId'),
                    server_id=volume_attachment.get('serverId'),
                    device=volume_attachment.get('device'))
                va_list.append(va)
        else:
            volume_attachment = json_dict.get('volumeAttachment')
            va_list.append(
                VolumeAttachment(
                    id_=volume_attachment.get('id'),
                    volume_id=volume_attachment.get('volumeId'),
                    server_id=volume_attachment.get('serverId'),
                    device=volume_attachment.get('device')))
            va_list.append(va)
        return va_list

