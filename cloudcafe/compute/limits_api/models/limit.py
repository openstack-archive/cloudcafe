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

from cafe.engine.models.base import AutoMarshallingModel, \
    AutoMarshallingListModel
from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.common.equality_tools import EqualityTools


class TenantLimits(AutoMarshallingModel):

    def __init__(self, rate_limits, absolute_limits):
        super(TenantLimits, self).__init__()
        self.rate_limits = rate_limits
        self.absolute_limits = absolute_limits

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("{0}: {1}".format(prop, self.__dict__[prop]))
            return "limits: [{properties}]".format(
                properties=', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        # Escape any backslashes in the string or JSON parsing fails
        serialized_str = serialized_str.replace('\\', '\\\\')
        json_dict = json.loads(serialized_str)
        rate_limits = RateLimits._json_to_obj(json_dict['limits']['rate'])
        absolute_limits = AbsoluteLimits._json_to_obj(
            json_dict['limits']['absolute'])
        return TenantLimits(rate_limits=rate_limits,
                            absolute_limits=absolute_limits)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        root = ET.fromstring(serialized_str)
        cls._remove_xml_etree_namespace(
            root, 'http://docs.openstack.org/common/api/v1.0')
        cls._remove_xml_etree_namespace(
            root, 'http://docs.openstack.org/common/api/v1.1')
        rate_element_list = root.find('rates').findall('rate')
        rate_limits = RateLimits._xml_to_obj(rate_element_list)

        absolute_list = root.find('absolute')
        cls._remove_xml_etree_namespace(
            absolute_list, Constants.XML_API_ATOM_NAMESPACE)
        used = 'http://docs.openstack.org/compute/ext/used_limits/api/v1.1'
        cls._remove_xml_etree_namespace(absolute_list, used)
        absolute_limits = AbsoluteLimits._xml_to_obj(absolute_list)

        return TenantLimits(
            rate_limits=rate_limits, absolute_limits=absolute_limits)

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        return not self == other


class RateLimits(AutoMarshallingListModel):

    def __init__(self):
        super(RateLimits, self).__init__()

    @classmethod
    def _json_to_obj(cls, limits_json_list):
        rate_limits = RateLimits()
        for rate_limit in limits_json_list:
            rate_limit = RateLimit._json_to_obj(rate_limit)
            rate_limits.append(rate_limit)
        return rate_limits

    @classmethod
    def _xml_to_obj(cls, rate_element_list):
        rate_limits = RateLimits()
        for rate_element in rate_element_list:
            rate_limit = RateLimit._xml_to_obj(rate_element)
            rate_limits.append(rate_limit)
        return rate_limits


class RateLimit(AutoMarshallingModel):

    def __init__(self, regex=None, uri=None, limits=None):
        super(RateLimit, self).__init__()
        self.regex = regex
        self.uri = uri
        self.limits = limits

    @classmethod
    def _json_to_obj(cls, json_dict):
        limits = Limits._json_to_obj(json_dict.get('limit'))
        return RateLimit(regex=json_dict.get('regex'),
                         uri=json_dict.get('uri'), limits=limits)

    @classmethod
    def _xml_to_obj(cls, element):

        limit_element_list = element.findall('limit')
        limits = Limits._xml_to_obj(limit_element_list)
        rate_limit_dict = element.attrib
        return RateLimit(regex=rate_limit_dict.get('regex'),
                         uri=rate_limit_dict.get('uri'), limits=limits)


class Limits(AutoMarshallingListModel):

    def __init__(self):
        super(Limits, self).__init__()

    @classmethod
    def _json_to_obj(cls, limits_json_list):
        limits = Limits()
        for limit_json in limits_json_list:
            limit = Limit._json_to_obj(limit_json)
            limits.append(limit)
        return limits

    @classmethod
    def _xml_to_obj(cls, limit_element_list):
        limits = Limits()
        for limit_element in limit_element_list:
            limit = Limit._xml_to_obj(limit_element)
            limits.append(limit)
        return limits


class Limit(AutoMarshallingModel):

    def __init__(self, next_available=None, unit=None, remaining=None,
                 value=None, verb=None):
        super(Limit, self).__init__()
        self.next_available = next_available
        self.unit = unit
        self.remaining = remaining
        self.value = value
        self.verb = verb

    @classmethod
    def _json_to_obj(cls, limit_json_dict):
        limit = Limit(next_available=limit_json_dict.get('next-available'),
                      unit=limit_json_dict.get('unit'),
                      remaining=limit_json_dict.get('remaining'),
                      value=limit_json_dict.get('value'),
                      verb=limit_json_dict.get('verb'))
        return limit

    @classmethod
    def _xml_to_obj(cls, limit_element):
        limit_dict = limit_element.attrib
        limit = Limit(next_available=limit_dict.get('next-available'),
                      unit=limit_dict.get('unit'),
                      remaining=int(limit_dict.get('remaining')),
                      value=int(limit_dict.get('value')),
                      verb=limit_dict.get('verb'))
        return limit


class AbsoluteLimits(AutoMarshallingModel):

    def __init__(
            self, max_server_meta=None, max_personality=None,
            total_private_networks_used=None, max_image_meta=None,
            max_personality_size=None, max_sec_group_rules=None,
            max_total_keypairs=None, total_cores_used=None,
            total_ram_used=None, total_instances_used=None,
            total_floating_ips_used=None, max_total_cores=None,
            total_sec_groups_used=None, max_total_private_networks=None,
            max_total_floating_ips=None, max_total_instances=None,
            max_total_ram_size=None, max_sec_groups=None):
        super(AbsoluteLimits, self).__init__()
        self.max_server_meta = max_server_meta
        self.max_personality = max_personality
        self.total_private_networks_used = total_private_networks_used
        self.max_image_meta = max_image_meta
        self.max_personality_size = max_personality_size
        self.max_sec_group_rules = max_sec_group_rules
        self.max_total_keypairs = max_total_keypairs
        self.total_cores_used = total_cores_used
        self.total_ram_used = total_ram_used
        self.total_instances_used = total_instances_used
        self.total_floating_ips_used = total_floating_ips_used
        self.max_total_cores = max_total_cores
        self.total_sec_groups_used = total_sec_groups_used
        self.max_total_private_networks = max_total_private_networks
        self.max_total_floating_ips = max_total_floating_ips
        self.max_total_instances = max_total_instances
        self.max_total_ram_size = max_total_ram_size
        self.max_sec_groups = max_sec_groups

    @classmethod
    def _json_to_obj(cls, limits_dict):
        abs_limits = AbsoluteLimits(
            max_server_meta=limits_dict.get('maxServerMeta'),
            max_personality=limits_dict.get('maxPersonality'),
            total_private_networks_used=limits_dict.get(
                'totalPrivateNetworksUsed'),
            max_image_meta=limits_dict.get('maxImageMeta'),
            max_personality_size=limits_dict.get('maxPersonalitySize'),
            max_sec_group_rules=limits_dict.get('maxSecurityGroupRules'),
            max_total_keypairs=limits_dict.get('maxTotalKeypairs'),
            total_cores_used=limits_dict.get('totalCoresUsed'),
            total_ram_used=limits_dict.get('totalRAMUsed'),
            total_instances_used=limits_dict.get('totalInstancesUsed'),
            max_sec_groups=limits_dict.get('maxSecurityGroups'),
            total_floating_ips_used=limits_dict.get(
                'totalFloatingIpsUsed'),
            max_total_cores=limits_dict.get('maxTotalCores'),
            total_sec_groups_used=limits_dict.get(
                'totalSecurityGroupsUsed'),
            max_total_private_networks=limits_dict.get(
                'maxTotalPrivateNetworks'),
            max_total_floating_ips=limits_dict.get('maxTotalFloatingIps'),
            max_total_instances=limits_dict.get('maxTotalInstances'),
            max_total_ram_size=limits_dict.get('maxTotalRAMSize'))
        return abs_limits

    @classmethod
    def _xml_to_obj(cls, absolute_limit_list):
        limits_dict = {}
        for element in absolute_limit_list.findall('limit'):
            attrib = element.attrib
            limits_dict[attrib.get('name')] = int(attrib.get('value'))

        abs_limits = AbsoluteLimits(
            max_server_meta=limits_dict.get('maxServerMeta'),
            max_personality=limits_dict.get('maxPersonality'),
            total_private_networks_used=limits_dict.get(
                'totalPrivateNetworksUsed'),
            max_image_meta=limits_dict.get('maxImageMeta'),
            max_personality_size=limits_dict.get('maxPersonalitySize'),
            max_sec_group_rules=limits_dict.get('maxSecurityGroupRules'),
            max_total_keypairs=limits_dict.get('maxTotalKeypairs'),
            total_cores_used=limits_dict.get('totalCoresUsed'),
            total_ram_used=limits_dict.get('totalRAMUsed'),
            total_instances_used=limits_dict.get('totalInstancesUsed'),
            max_sec_groups=limits_dict.get('maxSecurityGroups'),
            total_floating_ips_used=limits_dict.get(
                'totalFloatingIpsUsed'),
            max_total_cores=limits_dict.get('maxTotalCores'),
            total_sec_groups_used=limits_dict.get(
                'totalSecurityGroupsUsed'),
            max_total_private_networks=limits_dict.get(
                'maxTotalPrivateNetworks'),
            max_total_floating_ips=limits_dict.get('maxTotalFloatingIps'),
            max_total_instances=limits_dict.get('maxTotalInstances'),
            max_total_ram_size=limits_dict.get('maxTotalRAMSize'))
        return abs_limits
