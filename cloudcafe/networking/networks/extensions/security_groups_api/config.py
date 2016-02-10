"""
Copyright 2015 Rackspace

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

from cloudcafe.networking.networks.common.config import NetworkingBaseConfig


class SecurityGroupsConfig(NetworkingBaseConfig):
    """Security Groups and Rules configuration parameters"""

    SECTION_NAME = 'security_groups'

    @property
    def starts_with_name(self):
        """Network start name label for test runs"""
        return self.get("starts_with_name", "security_groups_test")

    @property
    def data_plane_delay(self):
        """
        Expected time in seconds for the data plane to apply a security
        group to a port
        """
        return int(self.get("data_plane_delay", 35))

    @property
    def max_secgroups_per_port(self):
        """
        Maximum number of security groups that can be assigned to a neutron
        port
        """
        return int(self.get("max_secgroups_per_port", 5))

    @property
    def max_rules_per_secgroup(self):
        """
        Maximum number of rules that can be assigned to a security group
        """
        return int(self.get("max_rules_per_secgroup", 20))

    @property
    def max_rules_per_tenant(self):
        """
        Maximum number of rules per tenant
        """
        return int(self.get("max_rules_per_tenant", 100))

    @property
    def max_secgroups_per_tenant(self):
        """
        Maximum number of security groups per tenant
        """
        return int(self.get("max_secgroups_per_tenant", 10))
