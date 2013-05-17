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
from cloudcafe.compute.servers_api.models.servers import Server


class Hypervisor(AutoMarshallingModel):

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Hypervisor object to compare with
        @type other: Hypervisor
        @return: True if Host objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Hypervisor object to compare with
        @type other: Hypervisor
        @return: True if Hypervisor objects are not equal, False otherwise
        @rtype: bool
        """
        return not self.__eq__(other)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a Hypervisor
        based on the json serialized_str
        passed in.
        @param serialized_str: JSON serialized string
        @type serialized_str: String
        @return: List of Hypervisors
        @rtype: List
        """
        json_dict = json.loads(serialized_str)
        hypervisors = []
        for hypervisor_dict in json_dict['hypervisors']:
            if 'servers' in hypervisor_dict.keys():
                servers = []
                for server_dict in hypervisor_dict['servers']:
                    servers.append(Server._dict_to_obj(server_dict))
                hypervisor_dict.update({"servers": servers})
            hypervisors.append(cls._dict_to_obj(hypervisor_dict))
        return hypervisors

    @classmethod
    def _dict_to_obj(cls, hypervisor_dict):
        hypervisor = Hypervisor(**hypervisor_dict)
        return hypervisor

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a Hypervisor
        based on the xml serialized_str
        passed in.
        @param serialized_str: XML serialized string
        @type serialized_str: String
        @return: List of Hypervisors
        @rtype: List
        """
        element = ET.fromstring(serialized_str)
        hypervisors = []
        for hypervisor in element.findall('hypervisor'):
            if "servers" in [elem.tag for elem in hypervisor.iter()]:
                for server in hypervisor.iter('server'):
                    servers = []
                    servers.append(Server._dict_to_obj(server.attrib))
                hypervisor.attrib.update({"servers": servers})
            hypervisor = cls._dict_to_obj(hypervisor.attrib)
            hypervisors.append(hypervisor)
        return hypervisors
