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


class FlavorExtraSpecs(AutoMarshallingDictModel):

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        specs = FlavorExtraSpecs()
        specs_dict = {item.tag: item.text for item in element.getchildren()}
        specs.update(specs_dict)
        return specs

    @classmethod
    def _json_to_obj(cls, json_body):
        metadata = FlavorExtraSpecs()
        meta_contents = json.loads(json_body)
        metadata.update(meta_contents.get('extra_specs'))
        return metadata

    @classmethod
    def _dict_to_obj(cls, json_dict):
        specs = FlavorExtraSpecs()
        specs.update(json_dict)
        return specs
