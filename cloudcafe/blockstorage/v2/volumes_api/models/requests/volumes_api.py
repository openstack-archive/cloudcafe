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


class Volume(AutoMarshallingModel):

    def __init__(
            self, size=None, volume_type=None, name=None,
            description=None, metadata=None, availability_zone=None):

        self.size = size
        self.volume_type = volume_type
        self.name = name
        self.description = description
        self.metadata = metadata or {}
        self.availability_zone = availability_zone

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())

    def _obj_to_json_dict(self):
        sub_dict = {}
        sub_dict["size"] = self.size
        sub_dict["volume_type"] = self.volume_type
        sub_dict["name"] = self.name
        sub_dict["description"] = self.description
        sub_dict["metadata"] = self.metadata
        sub_dict["availability_zone"] = self.availability_zone

        root_dict = {}
        root_dict['volume'] = self._remove_empty_values(sub_dict)
        return root_dict

    def _obj_to_xml_ele(self):
        element = ElementTree.Element('volume')
        attrs = {}
        attrs["size"] = str(self.size)
        attrs["volume_type"] = self.volume_type
        attrs["name"] = self.name
        attrs["description"] = self.description
        attrs["availability_zone"] = self.availability_zone
        element = self._set_xml_etree_element(element, attrs)

        if len(self.metadata.keys()) > 0:
            metadata_element = ElementTree.Element('metadata')
            for key in self.metadata.keys():
                meta_element = ElementTree.Element('meta')
                meta_element.set('key', key)
                meta_element.text = self.metadata[key]
                metadata_element.append(meta_element)
            element.append(metadata_element)

        return element

    def _obj_to_xml(self):
        return ElementTree.tostring(self._obj_to_xml_ele())


class VolumeSnapshot(AutoMarshallingModel):

    def __init__(
            self, volume_id, force=True, name=None,
            description=None):

        self.volume_id = volume_id
        self.name = name
        self.description = description
        self.force = force

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())

    def _obj_to_json_dict(self):
        attrs = {}
        attrs["snapshot"] = {}

        sub_attrs = {}
        sub_attrs["volume_id"] = self.volume_id
        sub_attrs["name"] = self.display_name
        sub_attrs["description"] = self.display_description
        sub_attrs["force"] = self.force
        return self._remove_empty_values(attrs)

    def _obj_to_xml(self):
        return ElementTree.tostring(self._obj_to_xml_ele())

    def _obj_to_xml_ele(self):
        element = ElementTree.Element('snapshot')
        attrs = {}
        attrs["volume_id"] = self.volume_id
        attrs["name"] = self.display_name
        attrs["description"] = self.display_description
        attrs["force"] = str(self.force)
        element = self._set_xml_etree_element(element, attrs)
        return element
