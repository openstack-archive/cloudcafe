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


class Host(AutoMarshallingModel):

    def __init__(self, name, service, zone):
        self.name = name
        self.service = service
        self.zone = zone

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Host object to compare with
        @type other: Host
        @return: True if Host objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Host object to compare with
        @type other: Host
        @return: True if Host objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if 'host' in json_dict.keys():
            host = cls._dict_to_obj(json_dict['host'])
            return host

        if 'hosts' in json_dict.keys():
            hosts = []
            for host_dict in json_dict['hosts']:
                hosts.append(cls._dict_to_obj(host_dict['host']))
            return hosts

    @classmethod
    def _dict_to_obj(cls, json_dict):
        host = Host(json_dict.get('host_name'), json_dict.get('service'),
                    json_dict.get('zone'))
        return host

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Host based on the xml serialized_str
        passed in.'''
        element = ET.fromstring(serialized_str)

        if element.tag == 'host':
            host = cls._xml_ele_to_obj(element)
            return host

        if element.tag == 'hosts':
            hosts = []
            for host in element.findall('host'):
                host = cls._xml_ele_to_obj(host)
                hosts.append(host)
            return hosts

    @classmethod
    def _xml_ele_to_obj(cls, element):
        host_dict = element.attrib
        host = Host(host_dict.get('host_name'), host_dict.get('service'),
                    host_dict.get('zone'))
        return host
