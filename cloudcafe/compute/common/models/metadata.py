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

from cafe.engine.models.base import AutoMarshallingDictModel
from cloudcafe.compute.common.constants import Constants


class Metadata(AutoMarshallingDictModel):

    def _obj_to_json(self):
        return json.dumps({'metadata': self})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('metadata')
        element.set('xmlns', Constants.XML_API_NAMESPACE)

        for key, value in self.items():
            meta_element = ET.Element('meta')
            meta_element.set('key', key)
            meta_element.text = value
            element.append(meta_element)
        xml += ET.tostring(element)
        return xml

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        metadata = Metadata()
        meta_items = element.findall('meta')
        meta_dict = {meta.attrib['key']: meta.text for meta in meta_items}
        metadata.update(meta_dict)
        return metadata

    @classmethod
    def _json_to_obj(cls, json_body):
        metadata = Metadata()
        meta_contents = json.loads(json_body)
        metadata.update(meta_contents.get('metadata'))
        return metadata

    @classmethod
    def _dict_to_obj(cls, json_dict):
        metadata = Metadata()
        metadata.update(json_dict)
        return metadata


class MetadataItem(AutoMarshallingDictModel):

    def _obj_to_json(self):
        return json.dumps({'meta': self})

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('meta')

        for key, value in self.items():
            element.set('key', key)
            element.text = value
        xml += ET.tostring(element)
        return xml

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)

        meta_item = MetadataItem()
        meta_item[element.attrib.get('key')] = element.text
        return meta_item

    @classmethod
    def _json_to_obj(cls, json_body):
        metadata = MetadataItem()
        meta_contents = json.loads(json_body)
        metadata.update(meta_contents.get('meta'))
        return metadata
