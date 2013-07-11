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


class IpRange(AutoMarshallingModel):

    def __init__(self, cidr=None):
        self.cidr = cidr

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return IpRange(json_dict.get('cidr'))

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        cidr = xml_ele.find('cidr').text
        return IpRange(cidr=cidr)


class SecurityGroupRule(AutoMarshallingModel):

    def __init__(self, id=None, from_port=None, ip_protocol=None, to_port=None,
                 parent_group_id=None, ip_range=None):
        self.id = id
        self.from_port = from_port
        self.ip_protocol = ip_protocol
        self.to_port = to_port
        self.parent_group_id = parent_group_id
        self.ip_range = ip_range

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a SecurityGroupRule
         based on the json serialized_str passed in.
        @param serialized_str: json serialized string.
        @type serialized_str: String.
        @return: SecurityGroupRule.
        @rtype: SecurityGroupRule.
         """
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get('security_group_rule'))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        ip_range = IpRange._dict_to_obj(json_dict.get('ip_range'))
        return SecurityGroupRule(id=json_dict.get('id'),
                                 from_port=json_dict.get('from_port'),
                                 ip_protocol=json_dict.get('ip_protocol'),
                                 to_port=json_dict.get('to_port'),
                                 parent_group_id=
                                 json_dict.get('parent_group_id'),
                                 ip_range=ip_range)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a SecurityGroupRule
         based on the xml serialized_str passed in.
        @param serialized_str: xml serialized string.
        @type serialized_str: String.
        @return: SecurityGroupRule.
        @rtype: SecurityGroupRule.
         """
        element = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(
            element, Constants.XML_API_NAMESPACE)
        sec_group_rule = cls._xml_ele_to_obj(element)
        return sec_group_rule

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        id = xml_ele.attrib.get('id')
        parent_group_id = xml_ele.attrib.get('parent_group_id')
        ip_range = IpRange._xml_ele_to_obj(xml_ele.find('ip_range'))
        from_port = xml_ele.find('from_port').text
        to_port = xml_ele.find('to_port').text
        ip_protocol = xml_ele.find('ip_protocol').text
        return SecurityGroupRule(id=id, from_port=from_port,
                                 ip_protocol=ip_protocol,
                                 to_port=to_port,
                                 parent_group_id=parent_group_id,
                                 ip_range=ip_range)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: SecurityGroupRule object to compare with
        @type other: SecurityGroupRule
        @return: True if SecurityGroupRule objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: SecurityGroupRule object to compare with
        @type other: SecurityGroupRule
        @return: True if SecurityGroupRule objects
         are not equal, False otherwise
        @rtype: bool
        """
        return not EqualityTools.are_objects_equal(self, other)
