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
from cloudcafe.compute.hosts_api.models.resources import Resource


class Host(AutoMarshallingModel):

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

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
        return not self.__eq__(other)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a Host or a collection of Hosts
         based on the json serialized_str passed in.
        @param serialized_str: json serialized string.
        @type serialized_str: String.
        @return: Host or List of Hosts.
        @rtype: Host or List.
         """
        json_dict = json.loads(serialized_str)
        if 'host' in json_dict.keys():
            resources = []
            for resource in json_dict.get("host"):
                resources.append(
                    Resource._dict_to_obj(resource.get("resource")))
            host = Host(resources=resources)
            return host

        if 'hosts' in json_dict.keys():
            hosts = []
            for host_dict in json_dict.get("hosts"):
                hosts.append(cls._dict_to_obj(host_dict))
            return hosts

    @classmethod
    def _dict_to_obj(cls, host_dict):
        """
        @summary: Returns an instance of a Host based on Host dictionary
         passed.
        @param host_dict: Host dictionary.
        @type host_dict: Dictionary.
        @return: Host.
        @rtype: Host.
         """
        host = Host(**host_dict)
        return host

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a Host or a collection of Hosts
         based on the xml serialized_str passed in.
        @param serialized_str: xml serialized string.
        @type serialized_str: String.
        @return: Host or a List of Hosts.
        @rtype: Host or List.
         """
        element = ET.fromstring(serialized_str)

        if element.tag == 'host':
            resources = []
            for resource in element._children:
                resources.append(Resource._xml_to_obj(resource))
            host = Host(resources=resources)
            return host

        if element.tag == 'hosts':
            hosts = []
            for host in element.findall('host'):
                host = cls._xml_ele_to_obj(host)
                hosts.append(host)
            return hosts

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """
        @summary: Returns an instance of a Host based on Element
         passed.
        @param element: xml element.
        @type element: Element.
        @return: Host.
        @rtype: Host.
         """
        host = Host(**element.attrib)
        return host
