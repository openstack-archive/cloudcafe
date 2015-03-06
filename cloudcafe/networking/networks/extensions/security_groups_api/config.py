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

from cloudcafe.networking.networks.common.config import NetworkingBaseConfig


class SecurityGroupsConfig(NetworkingBaseConfig):
    """Security Groups and Rules configuration parameters"""

    SECTION_NAME = 'security_groups'

    @property
    def starts_with_name(self):
        """Network start name label for test runs"""
        return self.get("starts_with_name", "security_groups_test")

    @property
    def rules_per_group(self):
        """Security Group Rules per group quota"""
        return int(self.get("rules_per_group", 20))

    @property
    def rules_per_tenant(self):
        """Security Group Rules per tenant quota"""
        return int(self.get("rules_per_tenant", 100))

    @property
    def groups_per_tenant(self):
        """Security Groups per tenant quota"""
        return int(self.get("groups_per_tenant", 10))

    @property
    def groups_per_port(self):
        """Security Groups per port quota"""
        return int(self.get("groups_per_port", 5))
