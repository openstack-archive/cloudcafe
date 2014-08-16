"""
Copyright 2014 Rackspace

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

from cloudcafe.common.models.configuration import ConfigSectionInterface


class NetsSubnetsPortsConfig(ConfigSectionInterface):

    SECTION_NAME = 'nets_subnets_ports'

    @property
    def isolated_subnets_cidr(self):
        """
        The cidr block to allocate isolated ipv4 subnets from
        """
        return self.get("isolated_subnets_cidr", "10.100.0.0/16")

    @property
    def isolated_subnets_mask_bits(self):
        """
        The mask bits for isolated ipv4 subnets
        """
        return int(self.get("isolated_subnets_mask_bits", 24))

    @property
    def isolated_subnets_v6_cidr(self):
        """
        The cidr block to allocate isolated ipv6 subnets from
        """
        return self.get("isolated_subnets_v6_cidr", "2003::/64")

    @property
    def isolated_subnets_v6_mask_bits(self):
        """
        The mask bits for isolated ipv6 subnets
        """
        return int(self.get("isolated_subnets_v6_mask_bits", 96))

    @property
    def public_network_id(self):
        """
        The uuid of the public network
        """
        return self.get("public_network_id",
                        "00000000-0000-0000-0000-000000000000")

    @property
    def service_network_id(self):
        """
        The uuid of the service network
        """
        return self.get("service_network_id",
                        "11111111-1111-1111-1111-111111111111")
