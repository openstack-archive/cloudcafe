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


class GetConsoleOutput(AutoMarshallingModel):
    """
    Get Console Output Request Object
    """

    def __init__(self, length):
        self.length = length

    def _obj_to_json(self):
        json_dict = {"length": str(self.length)}
        return json.dumps({"os-getConsoleOutput": json_dict})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element("os-getConsoleOutput")
        element.set("length", str(self.length))
        xml += ET.tostring(element)
        return xml
