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


class PortsConfig(NetworkingBaseConfig):
    """Port is the resource"""

    SECTION_NAME = 'ports'

    @property
    def starts_with_name(self):
        """Port start name label for test runs"""
        return self.get("starts_with_name", "test_port")

    @property
    def multiple_ports(self):
        """Test multiple ports smoke test ports number"""
        return int(self.get("multiple_ports", 10))

    @property
    def ports_per_network(self):
        """Ports per network quota"""
        return int(self.get("ports_per_network", 250))

    @property
    def test_quotas(self):
        """Flag for running the ports quotas tests"""
        return self.get_boolean("test_quotas", False)

    @property
    def fixed_ips_per_port(self):
        """Ports fixed IPs quota"""
        return int(self.get("fixed_ips_per_port", 4))

    @property
    def use_wait(self):
        """Flag to enable/disable the ports create wait time"""
        return self.get_boolean("use_wait", True)

    @property
    def port_create_wait(self):
        """Ports create delay time used at behavior method for rate-limits"""
        return int(self.get("port_create_wait", 20))

    @property
    def port_update_wait(self):
        """Ports update delay time used at behavior method for rate-limits"""
        return int(self.get("port_update_wait", 20))

    @property
    def port_delete_wait(self):
        """Ports delete delay time used at behavior method for rate-limits"""
        return int(self.get("port_delete_wait", 20))
