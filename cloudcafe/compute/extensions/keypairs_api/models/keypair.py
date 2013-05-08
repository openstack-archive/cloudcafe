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


class Keypair(AutoMarshallingModel):

    def __init__(self, public_key, name, fingerprint):
        self.public_key = public_key
        self.name = name
        self.fingerprint = fingerprint

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Keypair(json_dict.get('public_key'),
                       json_dict.get('name'),
                       json_dict.get('fingerprint'))

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


class Keypairs(Keypair):

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplemented

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = []
        json_dict = json.loads(serialized_str)
        key_list = json_dict.get('keypairs')

        for key in key_list:
            ret.append(Keypair(key.get('public_key'),
                               key.get('name'),
                               key.get('fingerprint')))
        return ret
