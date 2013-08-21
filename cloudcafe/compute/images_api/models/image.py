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

from cafe.engine.models.base import AutoMarshallingModel, \
    AutoMarshallingListModel
from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.compute.common.models.link import Links
from cloudcafe.compute.common.models.metadata import Metadata


class Image(AutoMarshallingModel):

    def __init__(self, disk_config=None, size=None, id=None, name=None,
                 status=None, updated=None, created=None, min_disk=None,
                 min_ram=None, progress=None, links=None, metadata=None,
                 server=None):
        super(Image, self).__init__()
        self.disk_config = disk_config
        self.size = size
        self.id = id
        self.name = name
        self.status = status
        self.updated = updated
        self.created = created
        self.min_disk = min_disk
        self.min_ram = min_ram
        self.progress = progress
        self.links = links
        self.metadata = metadata
        self.server = server

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("{0}: {1}".format(prop, self.__dict__[prop]))
        return "image: [{properties}]".format(properties=', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        image = cls._dict_to_obj(json_dict['image'])
        return image

    @classmethod
    def _dict_to_obj(cls, json_dict):

        links = None
        metadata = None
        server = None
        if 'links' in json_dict:
            links = Links._dict_to_obj(json_dict['links'])
        if 'metadata' in json_dict:
            metadata = Metadata._dict_to_obj(json_dict['metadata'])
        if 'server' in json_dict:
            # Prevents circular import issue import just in time
            from cloudcafe.compute.servers_api.models.servers import ServerMin
            server = ServerMin._dict_to_obj(json_dict['server'])

        image = Image(
            disk_config=json_dict.get('OS-DCF:diskConfig'),
            size=json_dict.get('OS-EXT-IMG-SIZE:size'),
            id=json_dict.get('id'), name=json_dict.get('name'),
            status=json_dict.get('status'),
            updated=json_dict.get('updated'),
            created=json_dict.get('created'),
            min_disk=json_dict.get('minDisk'),
            min_ram=json_dict.get('minRam'),
            progress=json_dict.get('progress'),
            links=links, metadata=metadata, server=server)
        return image

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """Returns an instance of a Image based on the xml passed in."""
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_NAMESPACE)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_ATOM_NAMESPACE)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_DISK_CONFIG_NAMESPACE)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_SIZE_NAMESPACE)
        image = cls._xml_ele_to_obj(element)
        return image

    @classmethod
    def _xml_ele_to_obj(cls, element):
        image_dict = element.attrib
        if 'minDisk' in image_dict:
            image_dict['minDisk'] = (image_dict.get('minDisk')
                                     and int(image_dict.get('minDisk')))
        if 'progress' in image_dict:
            image_dict['progress'] = (image_dict.get('progress')
                                      and int(image_dict.get('progress')))
        if 'minRam' in image_dict:
            image_dict['minRam'] = (image_dict.get('minRam')
                                    and int(image_dict.get('minRam')))

        links = None
        metadata = None
        server = None
        if element.find('link') is not None:
            links = Links._xml_ele_to_obj(element)
        if element.find('metadata') is not None:
            metadata = Metadata._xml_ele_to_obj(element.find('metadata'))
        if element.find('server') is not None:
            # Prevents circular import issue import just in time
            from cloudcafe.compute.servers_api.models.servers import ServerMin
            server = ServerMin._xml_ele_to_obj(element)

        image = Image(
            disk_config=image_dict.get('diskConfig'),
            size=image_dict.get('size'), id=image_dict.get('id'),
            name=image_dict.get('name'), status=image_dict.get('status'),
            updated=image_dict.get('updated'),
            created=image_dict.get('created'),
            min_disk=image_dict.get('minDisk'),
            min_ram=image_dict.get('minRam'),
            progress=image_dict.get('progress'),
            links=links, metadata=metadata, server=server)
        return image


class Images(AutoMarshallingListModel):

    image_type = Image

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('images'))

    @classmethod
    def _list_to_obj(cls, image_dict_list):
        images = Images()
        for image_dict in image_dict_list:
            image = cls.image_type._dict_to_obj(image_dict)
            images.append(image)
        return images

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        if element.tag != 'images':
            return None
        return cls._xml_list_to_obj(element.findall('image'))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        images = Images()
        for ele in xml_list:
            images.append(cls.image_type._xml_ele_to_obj(ele))
        return images


class ImageMin(Image):

    def __init__(self, id, name, links):
        super(ImageMin, self).__init__()
        self.id = id
        self.name = name
        self.links = links

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        return not self == other

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """Helper method to turn ElementTree instance to Image instance."""
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        image_dict = element.attrib

        if element.find('link') is not None:
            links = Links._xml_ele_to_obj(element)
        else:
            links = None
        image_min = ImageMin(id=image_dict.get('id'),
                             name=image_dict.get('name'), links=links)
        return image_min

    @classmethod
    def _dict_to_obj(cls, json_dict):
        if 'links' in json_dict:
            links = Links(json_dict.get('links'))
        else:
            links = None
        image_min = ImageMin(id=json_dict.get('id'),
                             name=json_dict.get('name'), links=links)
        return image_min


class ImageMins(Images):

    image_type = ImageMin
