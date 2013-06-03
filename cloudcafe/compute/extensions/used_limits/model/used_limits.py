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

from cloudcafe.compute.common.equality_tools import EqualityTools

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.extensions.used_limits.model.absolute import Absolute


class Rate(AutoMarshallingModel):

    def __init__(self, regex=None,
                 limit=None, uri=None):
        super(Rate, self).__init__()
        self.regex = regex
        self.limit = limit
        self.uri = uri

    @classmethod
    def _dict_to_obj(cls, rate_dict):
        rate = rate_dict[0]
        limits = []
        for limit in rate.get('limit'):
            limits.append(Limit._dict_to_obj(limit))
        return Rate(rate.get('regex'), limits,
                    rate.get('uri'))

    @classmethod
    def _xml_ele_to_obj(cls, rates):
        rate = rates.findall('rate')[0]
        limits = []
        for limit in rate.findall('limit'):
                limits.append(Limit._dict_to_obj(limit.attrib))
        return Rate(rate.attrib.get('regex'), limits,
                    rate.attrib.get('uri'))


class Limit(AutoMarshallingModel):

    def __init__(self, next_available=None,
                 unit=None, verb=None,
                 remaining=None, value=None):
        super(Limit, self).__init__()
        self.next_available = next_available
        self.unit = unit
        self.verb = verb
        self.remaining = remaining
        self.value = value

    @classmethod
    def _dict_to_obj(cls, limit_dict):
        return Limit(limit_dict.get('next-available'),
                     limit_dict.get('unit'), limit_dict.get('verb'),
                     limit_dict.get('remaining'), limit_dict.get('value'))


class UsedLimits(AutoMarshallingModel):

    def __init__(self, rate=None, absolute=None):
        super(UsedLimits, self).__init__()
        self.rate = rate
        self.absolute = absolute

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: UsedLimits object to compare with
        @type other: UsedLimits
        @return: True if UsedLimits objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: UsedLimits object to compare with
        @type other: UsedLimits
        @return: True if UsedLimits objects are not equal, False otherwise
        @rtype: bool
        """
        return not self.__eq__(other)

    @classmethod
    def _json_to_obj(cls, serialized_str):

        json_dict = json.loads(serialized_str)
        rate_dict = json_dict.get('limits').get('rate')
        rates = Rate._dict_to_obj(rate_dict)
        absolute_dict = json_dict.get('limits').get('absolute')
        absolute = Absolute._dict_to_obj(absolute_dict)
        usedLimitsForAdmin = UsedLimits(rates, absolute)
        return usedLimitsForAdmin

    @classmethod
    def _xml_to_obj(cls, serialized_str):

        limits = ET.fromstring(serialized_str)
        rates_xml = limits.find('rates')
        rates = Rate._xml_ele_to_obj(rates_xml)
        absolute_xml = limits.find('absolute')
        absolute = Absolute._xml_ele_to_obj(absolute_xml)
        usedLimitsForAdmin = UsedLimits(rates, absolute)
        return usedLimitsForAdmin
