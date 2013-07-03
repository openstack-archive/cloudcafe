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

    def __init__(self, max_server_meta=None, max_personality=None,
                 max_image_meta=None, max_personality_size=None,
                 max_security_group_rules=None, max_total_keypairs=None,
                 total_ram_used=None, total_instances_used=None,
                 max_security_groups=None, total_floating_ips_used=None,
                 max_total_cores=None, total_security_groups_used=None,
                 max_total_floating_ips=None, max_total_instances=None,
                 total_cores_used=None, max_total_ram_size=None):
        super(Absolute, self).__init__()
        self.max_server_meta = max_server_meta
        self.max_personality = max_personality
        self.max_image_meta = max_image_meta
        self.max_personality_size = max_personality_size
        self.max_security_group_rules = max_security_group_rules
        self.max_total_key_pairs = max_total_keypairs
        self.total_ram_used = total_ram_used
        self.total_instances_used = total_instances_used
        self.max_security_groups = max_security_groups
        self.total_floating_ips_used = total_floating_ips_used
        self.max_total_cores = max_total_cores
        self.total_security_groups_used = total_security_groups_used
        self.max_total_floating_ips = max_total_floating_ips
        self.max_total_instances = max_total_instances
        self.total_cores_used = total_cores_used
        self.max_total_ram_size = max_total_ram_size

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
