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

from cafe.engine.models.base import AutoMarshallingModel


class Absolute(AutoMarshallingModel):

    def __init__(self, maxServerMeta=None, maxPersonality=None,
                 maxImageMeta=None, maxPersonalitySize=None,
                 maxSecurityGroupRules=None, maxTotalKeypairs=None,
                 totalRAMUsed=None, totalInstancesUsed=None,
                 maxSecurityGroups=None, totalFloatingIpsUsed=None,
                 maxTotalCores=None, totalSecurityGroupsUsed=None,
                 maxTotalFloatingIps=None, maxTotalInstances=None,
                 totalCoresUsed=None, maxTotalRAMSize=None):
        super(Absolute, self).__init__()
        self.maxServerMeta = maxServerMeta
        self.maxPersonality = maxPersonality
        self.maxImageMeta = maxImageMeta
        self.maxPersonalitySize = maxPersonalitySize
        self.maxSecurityGroupRules = maxSecurityGroupRules
        self.maxTotalKeyPairs = maxTotalKeypairs
        self.totalRAMUsed = totalRAMUsed
        self.totalInstancesUsed = totalInstancesUsed
        self.maxSecurityGroups = maxSecurityGroups
        self.totalFloatingIPsUsed = totalFloatingIpsUsed
        self.maxTotalCores = maxTotalCores
        self.totalSecurityGroupsUsed = totalSecurityGroupsUsed
        self.maxTotalFloatingIps = maxTotalFloatingIps
        self.maxTotalInstances = maxTotalInstances
        self.totalCoresUsed = totalCoresUsed
        self.maxTotalRAMSize = maxTotalRAMSize

    @classmethod
    def _dict_to_obj(cls, absolute_dict):
        return Absolute(absolute_dict.get('maxServerMeta'),
                        absolute_dict.get('maxPersonality'),
                        absolute_dict.get('maxImageMeta'),
                        absolute_dict.get('maxPersonalitySize'),
                        absolute_dict.get('maxSecurityGroupRules'),
                        absolute_dict.get('maxTotalKeypairs'),
                        absolute_dict.get('totalRAMUsed'),
                        absolute_dict.get('totalInstancesUsed'),
                        absolute_dict.get('maxSecurityGroups'),
                        absolute_dict.get('totalFloatingIpsUsed'),
                        absolute_dict.get('maxTotalCores'),
                        absolute_dict.get('totalSecurityGroupsUsed'),
                        absolute_dict.get('maxTotalFloatingIps'),
                        absolute_dict.get('maxTotalInstances'),
                        absolute_dict.get('totalCoresUsed'),
                        absolute_dict.get('maxTotalRAMSize'))

    @classmethod
    def _xml_ele_to_obj(cls, absolute_xml):
        limit = absolute_xml.findall('limit')
        absolute_dict = dict((l.attrib['name'], l.attrib['value'])
                             for l in limit)
        return cls._dict_to_obj(absolute_dict)
