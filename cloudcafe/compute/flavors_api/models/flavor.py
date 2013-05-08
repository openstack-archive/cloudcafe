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
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.compute.common.constants import Constants
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
                 swap=None, rxtx_factor=None, links=None):
        """
        An object that represents a flavor.
        """
        self.id = id
        self.name = name
        self.ram = ram
        self.disk = disk
        self.vcpus = vcpus
        self.links = links

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of a Flavor based on the json serialized_str
        passed in.
        """
        json_dict = json.loads(serialized_str)

        if 'flavor' in json_dict.keys():
            flavor = cls._dict_to_obj(json_dict['flavor'])
            return flavor

        if 'flavors' in json_dict.keys():
            flavors = []
            for flavor_dict in json_dict['flavors']:
                flavor = cls._dict_to_obj(flavor_dict)
                flavors.append(flavor)
            return flavors

    @classmethod
    def _dict_to_obj(cls, flavor_dict):
        """Helper method to turn dictionary into Server instance."""
        flavor = Flavor(id=flavor_dict.get('id'),
                        name=flavor_dict.get('name'),
                        ram=flavor_dict.get('ram'),
                        disk=flavor_dict.get('disk'),
                        vcpus=flavor_dict.get('vcpus'))
        flavor.links = Links._dict_to_obj(flavor_dict['links'])
        return flavor

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        Returns an instance of a Flavor based on the xml serialized_str
        passed in.
        """
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_xml_etree_namespace(element,
                                        Constants.XML_API_ATOM_NAMESPACE)

        if element.tag == 'flavor':
            flavor = cls._xml_ele_to_obj(element)
            return flavor

        if element.tag == 'flavors':
            flavors = []
            for flavor in element.findall('flavor'):
                flavor = cls._xml_ele_to_obj(flavor)
                flavors.append(flavor)
            return flavors

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """Helper method to turn ElementTree instance to Flavor instance."""
        flavor_dict = element.attrib
        if 'vcpus' in flavor_dict:
            flavor_dict['vcpus'] = (flavor_dict.get('vcpus') and
                                    int(flavor_dict.get('vcpus')))
        if 'disk' in flavor_dict:
            flavor_dict['disk'] = (flavor_dict.get('disk') and
                                   int(flavor_dict.get('disk')))
        if 'rxtx_factor' in flavor_dict:
            flavor_dict['rxtx_factor'] = flavor_dict.get('rxtx_factor') \
                and float(flavor_dict.get('rxtx_factor'))
        if 'ram' in flavor_dict:
            flavor_dict['ram'] = flavor_dict.get('ram') \
                and int(flavor_dict.get('ram'))
        if 'swap' in flavor_dict:
            flavor_dict['swap'] = flavor_dict.get('swap') \
                and int(flavor_dict.get('swap'))

        links = Links._xml_ele_to_obj(element)
        flavor = Flavor(flavor_dict.get('id'), flavor_dict.get('name'),
                        flavor_dict.get('ram'), flavor_dict.get('disk'),
                        flavor_dict.get('vcpus'), flavor_dict.get('swap'),
                        flavor_dict.get('rxtx_factor'), links)
        return flavor

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Flavor object to compare with
        @type other: Flavor
        @return: True if Flavor objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other, ['links'])

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Flavor object to compare with
        @type other: Flavor
        @return: True if Flavor objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other


class FlavorMin(Flavor):
    """
    @summary: Represents minimum details of a flavor
    """
    def __init__(self, **kwargs):
        """Flavor Min has only id, name and links"""
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: FlavorMin object to compare with
        @type other: FlavorMin
        @return: True if FlavorMin objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other, ['links'])

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: FlavorMin object to compare with
        @type other: FlavorMin
        @return: True if FlavorMin objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """Helper method to turn ElementTree instance to Server instance."""
        flavor_dict = element.attrib
        flavor_min = FlavorMin(id=flavor_dict.get('id'),
                               name=flavor_dict.get('name'))
        flavor_min.links = Links._xml_ele_to_obj(element)
        return flavor_min

    @classmethod
    def _dict_to_obj(cls, flavor_dict):
        """Helper method to turn dictionary into Server instance."""
        flavor_min = FlavorMin(id=flavor_dict.get('id'),
                               name=flavor_dict.get('name'))
        flavor_min.links = Links._dict_to_obj(flavor_dict['links'])
        return flavor_min
