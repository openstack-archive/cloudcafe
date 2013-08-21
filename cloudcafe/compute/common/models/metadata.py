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

import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingDictModel
from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.common.equality_tools import EqualityTools


class Metadata(AutoMarshallingDictModel):


    def _obj_to_json(self):
        return self.__dict__

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('metadata')
        element.set('xmlns', Constants.XML_API_NAMESPACE)

        for key, value in self.__dict__.items():
            element = ET.Element('meta')
            element.set('xmlns', Constants.XML_API_NAMESPACE)

            element.set('key', key)
            element.text = value
            xml += ET.tostring(element)
        return xml

    @classmethod
    def _xml_to_obj(cls, element):
        meta_items = element.findall('meta')
        metadata = {meta.attrib['key']: meta.text for meta in meta_items}
        return metadata

    @classmethod
    def _json_to_obj(cls, json_dict):
        return json_dict

