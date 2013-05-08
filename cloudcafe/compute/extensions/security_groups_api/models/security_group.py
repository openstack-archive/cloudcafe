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
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get('security_group'))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return SecurityGroup(id=json_dict.get('id'),
                             name=json_dict.get('name'),
                             description=json_dict.get('description'),
                             rules=json_dict.get('rules'),
                             tenant_id=json_dict.get('tenant_id'))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplemented

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        raise NotImplemented

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
        raise NotImplemented

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = []
        json_dict = json.loads(serialized_str)
        groups = json_dict.get('security_groups')

        for group in groups:
            ret.append(SecurityGroup._dict_to_obj(group))
        return ret
