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
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.constants import Constants


class CreateVolume(AutoMarshallingModel):
    """
    Get Create Volume Request Object
    """

    def __init__(self, display_name, display_description, size, volume_type, metadata, availability_zone):
        self.display_name = display_name
        self.display_description = display_description
        self.size = size
        self.volume_type = volume_type
        self.metadata = metadata
        self.availability_zone = availability_zone

    def _obj_to_json(self):
        request_body = {
            "display_name": self.display_name,
            "display_description": self.display_description,
            "size": self.size,
            "volume_type": self.volume_type,
            "metadata": self.metadata,
            "availability_zone": self.availability_zone
         }
        return json.dumps({"volume": request_body})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element("volume")
        element.set("display_name", self.display_name)
        element.set("display_description", self.display_description)
        element.set("size", str(self.size))
        element.set("volume_type", self.volume_type)
        element.set("availability_zone", self.availability_zone)
        if self.metadata:
            metadata = ET.Element("metadata")
            for k, v in self.metadata.items():
                meta = ET.Element("meta")
                meta.set("key", k)
                meta.text = v
                metadata.append(meta)
            element.append(metadata)
        xml += ET.tostring(element)
        return xml

