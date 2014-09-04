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


class SubnetsConfig(NetworkingBaseConfig):
    """Subnet is the resource"""

    SECTION_NAME = 'subnets'

    @property
    def resource_build_attempts(self):
        """Number of times to try to create a resource"""
        return int(self.get("resource_build_attempts", 1))

    @property
    def keep_resources(self):
        """Flag for not deleting resources on tearDown"""
        return self.get_boolean("keep_resources", False)

    @property
    def keep_resources_on_failure(self):
        """Flag for not deleting resources w failures on tearDown"""
        return self.get_boolean("keep_resources_on_failure", False)

    @property
    def resource_create_timeout(self):
        """Seconds to wait for creating a resource"""
        return int(self.get("resource_create_timeout", 15))

    @property
    def resource_delete_timeout(self):
        """Seconds to wait for deleting a resource"""
        return int(self.get("resource_delete_timeout", 15))

    @property
    def starts_with_name(self):
        """Subnet start name label for test runs"""
        return self.get("name_starts_with", "test_subnet")

    @property
    def ipv4_suffix(self):
        """Subnet create default IPv4 suffix"""
        return int(self.get("ipv4_suffix", 24))

    @property
    def ipv4_suffix_max(self):
        """Subnet max suffix default value"""
        return int(self.get("ipv4_suffix_max", 30))

    @property
    def ipv4_prefix(self):
        """Subnet create default IPv4 prefix, can use * values
           for a random cidr create
        """
        return self.get("ipv4_prefix", "192.168.*.0")

    @property
    def private_ipv4_range(self):
        """Expected IPv4 private cidr range when creating subnets
           for ex. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
        """
        return self.get("private_ipv4_range", "192.168.0.0/16")

    @property
    def ipv6_suffix(self):
        """Subnet create default IPv6 suffix"""
        return int(self.get("ipv6_suffix", 64))

    @property
    def ipv6_suffix_max(self):
        """Subnet max suffix default value"""
        return int(self.get("ipv6_suffix_max", 64))

    @property
    def ipv6_prefix(self):
        """Subnet create default IPv6 prefix"""
        return self.get("ipv6_prefix", "fd00::")

    @property
    def private_ipv6_range(self):
        """Expected IPv6 private cidr range when creating subnets
           for ex. fd00::/8
        """
        return self.get("private_ipv6_range", "fd00::/8")
