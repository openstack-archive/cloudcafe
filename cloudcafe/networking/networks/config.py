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


class NetworkingEndpointConfig(ConfigSectionInterface):

    SECTION_NAME = 'networking_endpoint'

    @property
    def region(self):
        return self.get("region")

    @property
    def networking_endpoint_name(self):
        return self.get("networking_endpoint_name")

    @property
    def networking_endpoint_url(self):
        """Optional override of the Networking url"""
        return self.get("networking_endpoint_url", '')

    @property
    def header_tenant_id(self):
        """Optional tenant ID to set in client request headers"""
        return self.get("header_tenant_id", '')


class NetworkingAdminEndpointConfig(NetworkingEndpointConfig):
    """RackerAdmin API endpoint and name"""
    SECTION_NAME = 'networking_admin_endpoint'


class NetworkingAdminAuthConfig(UserAuthConfig):
    """Networking Admin endpoint and auth strategy, for ex. keystone"""
    SECTION_NAME = 'networking_admin_auth_config'


class NetworkingSecondUserConfig(UserConfig):

    SECTION_NAME = 'networking_secondary_user'


class NetworkingAdminUserConfig(UserConfig):

    SECTION_NAME = 'networking_admin_user'
