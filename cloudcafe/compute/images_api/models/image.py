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
from cloudcafe.compute.common.models.link import Links
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.common.models.metadata import Metadata


class Image(AutoMarshallingModel):

    def __init__(self, diskConfig, id, name, status, updated, created,
                 minDisk, minRam, progress, links=None, metadata=None,
                 server=None):
        self.diskConfig = diskConfig
        self.id = id
        self.name = name
        self.status = status
        self.updated = updated
        self.created = created
        self.minDisk = minDisk
        self.minRam = minRam
        self.progress = progress
        self.links = links
        self.metadata = metadata
        self.server = server

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Image object to compare with
        @type other: Image
        @return: True if Image objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Image object to compare with
        @type other: Image
        @return: True if Image objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    def __repr__(self):
        values = []
        for prop in __dict__:
            values.append("%s: %s" % (prop, __dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if 'image' in json_dict.keys():
            image = cls._dict_to_obj(json_dict['image'])
            return image

        if 'images' in json_dict.keys():
            images = []
            for image_dict in json_dict['images']:
                images.append(cls._dict_to_obj(image_dict))
            return images

    @classmethod
    def _dict_to_obj(cls, json_dict):
        image = Image(json_dict.get('OS-DCF:diskConfig'), json_dict.get('id'),
                      json_dict.get('name'), json_dict.get('status'),
                      json_dict.get('updated'), json_dict.get('created'),
                      json_dict.get('minDisk'), json_dict.get('minRam'),
                      json_dict.get('progress'))
        if 'links' in json_dict:
            image.links = Links._dict_to_obj(json_dict['links'])
        if 'metadata' in json_dict:
            image.metadata = Metadata._dict_to_obj(json_dict['metadata'])
        if 'server' in json_dict:
            from cloudcafe.compute.servers_api.models.servers import ServerMin
            image.server = ServerMin._dict_to_obj(json_dict['server'])
        return image

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Image based on the xml serialized_str
        passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_xml_etree_namespace(element,
                                        Constants.XML_API_ATOM_NAMESPACE)
        cls._set_clean_xml_etree_attrs(element.attrib,
                                       Constants.XML_API_DISK_CONFIG_NAMESPACE)

        if element.tag == 'image':
            image = cls._xml_ele_to_obj(element)
            return image

        if element.tag == 'images':
            images = []
            for image in element.findall('image'):
                image = cls._xml_ele_to_obj(image)
                images.append(image)
            return images

    @classmethod
    def _xml_ele_to_obj(cls, element):
        image_dict = element.attrib
        if 'minDisk' in image_dict:
            image_dict['minDisk'] = image_dict.get('minDisk') \
                and int(image_dict.get('minDisk'))
        if 'progress' in image_dict:
            image_dict['progress'] = image_dict.get('progress') \
                and int(image_dict.get('progress'))
        if 'minRam' in image_dict:
            image_dict['minRam'] = image_dict.get('minRam') \
                and int(image_dict.get('minRam'))

        links = None
        metadata = None
        server = None

        if element.find('link') is not None:
            links = Links._xml_ele_to_obj(element)
        if element.find('metadata') is not None:
            metadata = Metadata._xml_ele_to_obj(element)
        if element.find('server') is not None:
            '''To prevent circular import issue import just in time'''
            from cloudcafe.compute.servers_api.models.servers import ServerMin
            server = ServerMin._xml_ele_to_obj(element)

        image = Image(image_dict.get('diskConfig'),
                      image_dict.get('id'), image_dict.get('name'),
                      image_dict.get('status'), image_dict.get('updated'),
                      image_dict.get('created'), image_dict.get('minDisk'),
                      image_dict.get('minRam'), image_dict.get('progress'),
                      links, metadata, server)

        return image


class ImageMin(Image):
    """
    @summary: Represents minimum details of a image
    """
    def __init__(self, **kwargs):
        '''Image min should only have id, name and links '''
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: ImageMin object to compare with
        @type other: ImageMin
        @return: True if ImageMin objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: ImageMin object to compare with
        @type other: ImageMin
        @return: True if ImageMin objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Image instance.'''
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        image_dict = element.attrib
        image_min = ImageMin(**image_dict)
        image_min.links = Links._xml_ele_to_obj(element)
        return image_min

    @classmethod
    def _dict_to_obj(cls, json_dict):
        image_min = ImageMin(**json_dict)
        if 'links' in json_dict:
            image_min.links = Links(image_min.links)
        return image_min
