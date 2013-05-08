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
from cloudcafe.compute.common.equality_tools import EqualityTools


class MetadataItem(AutoMarshallingModel):
    """
    @summary: MetadataItem Request/Response Object for Server/Image
    """

    def __init__(self, metadata_dict):
        for key, value in metadata_dict.items():
            setattr(self, key, value)

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('meta')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        for key, value in (self._obj_to_dict(meta_obj=self)).items():
            element.set('key', key)
            element.text = value
        xml += ET.tostring(element)
        return xml

    @classmethod
    def _obj_to_dict(self, meta_obj):
        meta = {}
        for name in dir(meta_obj):
            value = getattr(meta_obj, name)
            if (not name.startswith('_') and not name.startswith('RO')
                    and not name.startswith('deser')
                    and not name.startswith('sele')
                    and not name.startswith('seria')):
                meta[name] = value
        return meta

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Initializes the object from xml response
        @param objectified_links: metadata item
        @type objectified_links: objectify.Element
        """

        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        metadata_item = cls._xml_ele_to_obj(element)
        return metadata_item

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """Helper method to turn ElementTree instance to metadata instance."""
        metadata_dict = {}
        metadata_dict[(element.attrib).get('key')] = element.text
        return MetadataItem(metadata_dict)

    @classmethod
    def _dict_to_object(cls, metadata_dict):
        """
        @summary: Initializes the object from json response
        @param metadata_dict: metadata items
        @type metadata_dict: dictionary
        """
        return MetadataItem(metadata_dict)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''
        Returns an instance of metadata item based on the json
        serialized_str passed in.
        '''
        json_dict = json.loads(serialized_str)
        if 'meta' in json_dict.keys():
            metadata_dict = json_dict['meta']
            return MetadataItem(metadata_dict)

    def __repr__(self):
        values = []
        for prop in __dict__:
            values.append("%s: %s" % (prop, __dict__[prop]))
        return '[' + ', '.join(values) + ']'


class Metadata(AutoMarshallingModel):
    ROOT_TAG = 'metadata'

    '''
    @summary: Metadata Request Object for Server/Image
    '''
    def __init__(self, metadata_dict):
        for key, value in metadata_dict.items():
            setattr(self, key, value)

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element('metadata')
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        for name in dir(self):
            value = getattr(self, name)
            if (not name.startswith('_') and not name.startswith('RO')
                    and not name.startswith('deser')
                    and not name.startswith('sele')
                    and not name.startswith('seria')):
                element.append(self._dict_to_xml(key=name, value=value))
        xml += ET.tostring(element)
        return xml

    @classmethod
    def _dict_to_xml(self, key, value):
        meta_element = ET.Element('meta')
        meta_element.set('key', key)
        meta_element.text = value
        return meta_element

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Initializes the object from xml response
        @param objectified_links: metadata details
        @type objectified_links: objectify.Element
        """

        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        metadata = cls._xml_ele_to_obj(element)
        return metadata

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """Helper method to turn ElementTree instance to metadata instance"""
        meta_dict = {}
        entity = element
        if entity.find('metadata') is not None:
            meta_list = entity.find("metadata").findall('meta')
            for each in meta_list:
                meta_dict[each.attrib['key']] = each.text
            return Metadata(meta_dict)
        if entity.tag == 'metadata':
            meta_list = entity.findall('meta')
            for each in meta_list:
                meta_dict[each.attrib['key']] = each.text
            return Metadata(meta_dict)

    @classmethod
    def _dict_to_obj(cls, metadata_dict):
        """
        @summary: Initializes the object from json response
        @param metadata_dict: metadata details
        @type metadata_dict: dictionary
        """
        return Metadata(metadata_dict)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of metadata based on the json
        serialized_str passed in.
        """
        json_dict = json.loads(serialized_str)
        if 'metadata' in json_dict.keys():
            metadata_dict = json_dict['metadata']
            return Metadata(metadata_dict)

    @classmethod
    def _obj_to_dict(self, meta_obj):
        meta = {}
        for name in dir(meta_obj):
            value = getattr(meta_obj, name)
            if (not name.startswith('_')
                    and not name.startswith('RO')
                    and not name.startswith('deser')
                    and not name.startswith('sele')
                    and not name.startswith('seria')):
                meta[name] = value
        return meta

    def __repr__(self):
        values = []
        for prop in __dict__:
            values.append("%s: %s" % (prop, __dict__[prop]))
        return '[' + ', '.join(values) + ']'

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Links object to compare with
        @type other: Links
        @return: True if Links objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Links object to compare with
        @type other: Links
        @return: True if Links objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other
