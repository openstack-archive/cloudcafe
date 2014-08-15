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

from cloudcafe.auth.config import UserAuthConfig, UserConfig
from cloudcafe.common.models.configuration import ConfigSectionInterface


class MarshallingConfig(ConfigSectionInterface):
    SECTION_NAME = 'marshalling'

    @property
    def serializer(self):
        return self.get("serialize_format")

    @property
    def deserializer(self):
        return self.get("deserialize_format")


class NetworksConfig(ConfigSectionInterface):

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


class NetworksEndpointConfig(ConfigSectionInterface):

    SECTION_NAME = 'networks_endpoint'

    @property
    def region(self):
        return self.get("region")

    @property
    def networks_endpoint_name(self):
        return self.get("networks_endpoint_name")

    @property
    def networks_endpoint_url(self):
        """Optional override of the Networks url"""
        return self.get("networks_endpoint_url")

    @property
    def header_tenant_id(self):
        """Optional tenant ID to set in client request headers"""
        return self.get("header_tenant_id")


class NetworksAdminEndpointConfig(NetworksEndpointConfig):
    """RackerAdmin API endpoint and name"""
    SECTION_NAME = 'networks_admin_endpoint'


class NetworksAdminAuthConfig(UserAuthConfig):
    """Networks Admin endpoint and auth strategy, for ex. keystone"""
    SECTION_NAME = 'networks_admin_auth_config'


class NetworksSecondUserConfig(UserConfig):

    SECTION_NAME = 'networks_secondary_user'


class NetworksAdminUserConfig(UserConfig):

    SECTION_NAME = 'networks_admin_user'
