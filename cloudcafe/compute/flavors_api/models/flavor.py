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
from cafe.engine.models.base import AutoMarshallingListModel
from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.compute.common.models.link import Links


class CreateFlavor(AutoMarshallingModel):

    def __init__(self, name=None, ram=None, vcpus=None,
                 disk=None, id=None, is_public=None):

        super(CreateFlavor, self).__init__()
        self.id = id
        self.name = name
        self.ram = ram
        self.disk = disk
        self.vcpus = vcpus
        self.is_public = is_public

    def _obj_to_json(self):
        ret = {'flavor': self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        ret['id'] = self.id
        ret['name'] = self.name
        ret['ram'] = int(self.ram)
        ret['disk'] = int(self.disk)
        ret['vcpus'] = int(self.vcpus)
        ret['os-flavor-access:is_public'] = self.is_public
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplemented

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        raise NotImplemented


class Flavor(AutoMarshallingModel):

    def __init__(self, id=None, name=None, ram=None, disk=None, vcpus=None,
                 swap=None, rxtx_factor=None, links=None,
                 ephemeral_disk=None):
        super(Flavor, self).__init__()
        self.id = id
        self.name = name
        self.ram = ram
        self.disk = disk
        self.vcpus = vcpus
        self.links = links
        self.swap = swap
        self.rxtx_factor = rxtx_factor
        self.ephemeral_disk = ephemeral_disk

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        flavor = cls._dict_to_obj(json_dict['flavor'])
        return flavor

    @classmethod
    def _dict_to_obj(cls, flavor_dict):
        flavor = Flavor(
            id=flavor_dict.get('id'), name=flavor_dict.get('name'),
            ram=flavor_dict.get('ram'), disk=flavor_dict.get('disk'),
            vcpus=flavor_dict.get('vcpus'), swap=flavor_dict.get('swap'),
            rxtx_factor=flavor_dict.get('rxtx_factor'),
            ephemeral_disk=flavor_dict.get('OS-FLV-EXT-DATA:ephemeral'),
            links=Links._dict_to_obj(flavor_dict['links']))
        return flavor

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_xml_etree_namespace(element,
                                        Constants.XML_API_ATOM_NAMESPACE)
        cls._remove_xml_etree_namespace(element,
                                        Constants.XML_FLAVOR_EXTRA_SPECS)
        flavor = cls._xml_ele_to_obj(element)
        return flavor

    @classmethod
    def _xml_ele_to_obj(cls, element):
        flavor_dict = element.attrib

        # XML data types differ from JSON, so we normalize here
        if 'vcpus' in flavor_dict:
            flavor_dict['vcpus'] = (flavor_dict.get('vcpus') and
                                    int(flavor_dict.get('vcpus')))
        if 'disk' in flavor_dict:
            flavor_dict['disk'] = (flavor_dict.get('disk') and
                                   int(flavor_dict.get('disk')))
        if 'rxtx_factor' in flavor_dict:
            flavor_dict['rxtx_factor'] = \
                (flavor_dict.get('rxtx_factor') and
                 float(flavor_dict.get('rxtx_factor')))
        if 'ram' in flavor_dict:
            flavor_dict['ram'] = (flavor_dict.get('ram')
                                  and int(flavor_dict.get('ram')))
        if 'swap' in flavor_dict:
            flavor_dict['swap'] = (flavor_dict.get('swap')
                                   and int(flavor_dict.get('swap')))
        if 'ephemeral' in flavor_dict:
            flavor_dict['ephemeral'] = (flavor_dict.get('ephemeral') and
                                        int(flavor_dict.get('ephemeral')))

        links = Links._xml_ele_to_obj(element)
        flavor = Flavor(
            id=flavor_dict.get('id'), name=flavor_dict.get('name'),
            ram=flavor_dict.get('ram'), disk=flavor_dict.get('disk'),
            vcpus=flavor_dict.get('vcpus'), swap=flavor_dict.get('swap'),
            rxtx_factor=flavor_dict.get('rxtx_factor'), links=links,
            ephemeral_disk=flavor_dict.get('ephemeral'))
        return flavor

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other, ['links'])

    def __ne__(self, other):
        return not self == other


class FlavorMin(Flavor):

    def __init__(self, id=None, links=None, name=None):

        super(FlavorMin, self).__init__()
        self.id = id
        self.links = links
        self.name = name

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other, ['links'])

    def __ne__(self, other):
        return not self == other

    @classmethod
    def _xml_ele_to_obj(cls, element):
        flavor_dict = element.attrib
        links = Links._xml_ele_to_obj(element)
        flavor_min = FlavorMin(id=flavor_dict.get('id'),
                               name=flavor_dict.get('name'),
                               links=links)
        return flavor_min

    @classmethod
    def _dict_to_obj(cls, flavor_dict):
        links = Links._dict_to_obj(flavor_dict['links'])
        flavor_min = FlavorMin(id=flavor_dict.get('id'),
                               name=flavor_dict.get('name'),
                               links=links)
        return flavor_min


class Flavors(AutoMarshallingListModel):

    flavor_type = Flavor

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get('flavors'))

    @classmethod
    def _list_to_obj(cls, flavor_dict_list):
        flavors = Flavors()
        for flavor_dict in flavor_dict_list:
            flavor = cls.flavor_type._dict_to_obj(flavor_dict)
            flavors.append(flavor)
        return flavors

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        if element.tag != 'flavors':
            return None
        return cls._xml_list_to_obj(element.findall('flavor'))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        flavors = Flavors()
        for ele in xml_list:
            flavors.append(cls.flavor_type._xml_ele_to_obj(ele))
        return flavors


class FlavorMins(Flavors):

    flavor_type = FlavorMin
