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


class NetworksConfig(NetworkingBaseConfig):
    """Network is the resource"""

    SECTION_NAME = 'networks'

    @property
    def public_network_id(self):
        """The uuid of the public network"""
        return self.get("public_network_id",
                        "00000000-0000-0000-0000-000000000000")

    @property
    def service_network_id(self):
        """The uuid of the service network (aka private)"""
        return self.get("service_network_id",
                        "11111111-1111-1111-1111-111111111111")

    @property
    def starts_with_name(self):
        """Network start name label for test runs"""
        return self.get("starts_with_name", "test_net")
