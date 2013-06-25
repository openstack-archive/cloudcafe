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
from cloudcafe.compute.extensions.security_groups_api.models.\
    security_group_rule import SecurityGroupRule


class SecurityGroup(AutoMarshallingModel):

    def __init__(self, id=None, name=None, description=None,
                 rules=None, tenant_id=None):
        self.name = name
        self.description = description
        self.rules = rules
        self.id = id
        self.tenant_id = tenant_id

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a SecurityGroup
         based on the json serialized_str passed in.
        @param serialized_str: json serialized string.
        @type serialized_str: String.
        @return: SecurityGroup.
        @rtype: SecurityGroup.
         """
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get('security_group'))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        rules = []
        for rule in json_dict.get('rules'):
            rules.append(SecurityGroupRule._dict_to_obj(rule))
        return SecurityGroup(id=json_dict.get('id'),
                             name=json_dict.get('name'),
                             description=json_dict.get('description'),
                             rules=rules,
                             tenant_id=json_dict.get('tenant_id'))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a SecurityGroup
         based on the xml serialized_str passed in.
        @param serialized_str: xml serialized string.
        @type serialized_str: String.
        @return: SecurityGroup.
        @rtype: SecurityGroup.
         """
        xml_ele = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(
            xml_ele, Constants.XML_API_NAMESPACE)
        return cls._xml_ele_to_obj(xml_ele)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        id = xml_ele.attrib.get('id')
        tenant_id = xml_ele.attrib.get('tenant_id')
        name = xml_ele.attrib.get('name')
        description = xml_ele.find('description').text
        rules = []
        for rule in xml_ele.find('rules').findall('rule'):
            rules.append(SecurityGroupRule._xml_ele_to_obj(rule))
        return SecurityGroup(id=id, name=name,
                             description=description,
                             rules=rules,
                             tenant_id=tenant_id)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Flavor object to compare with
        @type other: Flavor
        @return: True if Flavor objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Flavor object to compare with
        @type other: Flavor
        @return: True if Flavor objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other


class SecurityGroups(SecurityGroup):

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Returns a list of a SecurityGroup
         based on the xml serialized_str passed in.
        @param serialized_str: xml serialized string.
        @type serialized_str: String.
        @return: List.
        @rtype: List.
         """
        xml_ele = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(
            xml_ele, Constants.XML_API_NAMESPACE)
        groups = []
        for group in xml_ele.findall('security_group'):
            groups.append(SecurityGroup._xml_ele_to_obj(group))
        return groups

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Returns a list of a SecurityGroup
         based on the json serialized_str passed in.
        @param serialized_str: json serialized string.
        @type serialized_str: String.
        @return: List.
        @rtype: List.
         """
        ret = []
        json_dict = json.loads(serialized_str)
        groups = json_dict.get('security_groups')

        for group in groups:
            ret.append(SecurityGroup._dict_to_obj(group))
        return ret
