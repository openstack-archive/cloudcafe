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

from cafe.engine.models.base import AutoMarshallingModel


class VolumeAttachmentRequest(AutoMarshallingModel):

    def __init__(self, volume_id=None, device=None):
        super(VolumeAttachmentRequest, self).__init__()
        self.volume_id = volume_id
        self.device = device

    def _obj_to_json(self):
        data = {"volumeAttachment": self._obj_to_dict()}
        return json.dumps(data)

    def _obj_to_xml(self):
        element = ElementTree.Element('volumeAttachment')
        element = self._set_xml_etree_element(element, self._obj_to_dict())
        return ElementTree.tostring(element)

    def _obj_to_dict(self):
        return {"volumeId": self.volume_id, "device": self.device}
