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

from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.networking.networks.config import MarshallingConfig,\
    NetworksConfig, NetworksEndpointConfig, NetworksAdminEndpointConfig,\
    NetworksAdminAuthConfig, NetworksSecondUserConfig, \
    NetworksAdminUserConfig, UserAuthConfig, UserConfig
from cloudcafe.networking.networks.networks_api.client import NetworksClient
from cloudcafe.networking.networks.networks_api.config import NetworksAPIConfig
from cloudcafe.networking.networks.networks_api.behaviors \
    import NetworksAPIBehaviors
from cloudcafe.networking.networks.ports_api.client import PortsClient
from cloudcafe.networking.networks.ports_api.config import PortsAPIConfig
from cloudcafe.networking.networks.ports_api.behaviors import PortsAPIBehaviors
from cloudcafe.networking.networks.subnets_api.client import SubnetsClient
from cloudcafe.networking.networks.subnets_api.config import SubnetsAPIConfig
from cloudcafe.networking.networks.subnets_api.behaviors \
    import SubnetsAPIBehaviors


class _NetworksAuthComposite(MemoizedAuthServiceComposite):
    _networks_config = NetworksConfig
    _networks_endpoint_config = NetworksEndpointConfig
    _auth_endpoint_config = UserAuthConfig
    _auth_user_config = UserConfig

    def __init__(self):
        self.networks_endpoint_config = self._networks_endpoint_config()
        self.marshalling_config = MarshallingConfig()
        self._auth_endpoint_config = self._auth_endpoint_config()
        self._auth_user_config = self._auth_user_config()

        super(_NetworksAuthComposite, self).__init__(
            service_name=self.networks_endpoint_config.networks_endpoint_name,
            region=self.networks_endpoint_config.region,
            endpoint_config=self._auth_endpoint_config,
            user_config=self._auth_user_config)

        self.networks_url = self.public_url

        # Overriding the publicURL if networks_endpoint_url given
        if self.networks_endpoint_config.networks_endpoint_url:
            self.networks_url = \
                self.networks_endpoint_config.networks_endpoint_url

        # Ending backslash is not expected, removing if present
        if self.networks_url[-1] == '/':
            self.networks_url = self.networks_url[:-1]

        self.client_args = {
            'url': self.networks_url,
            'auth_token': self.token_id,
            'serialize_format': self.marshalling_config.serializer,
            'deserialize_format': self.marshalling_config.deserializer}

        if self.networks_endpoint_config.header_tenant_id:
            self.client_args.update(
                tenant_id=self.networks_endpoint_config.header_tenant_id)


class _NetworksAdminAuthComposite(_NetworksAuthComposite):
    _networks_endpoint_config = NetworksAdminEndpointConfig
    _auth_endpoint_config = NetworksAdminAuthConfig
    _auth_user_config = NetworksAdminUserConfig


class NetworksComposite(object):
    networks_auth_composite = _NetworksAuthComposite

    def __init__(self):
        auth_composite = self.networks_auth_composite()
        self.url = auth_composite.networks_url
        self.user = auth_composite._auth_user_config
        self.config = NetworksConfig()
        self.networks = NetworksAPIComposite(auth_composite)
        self.subnets = SubnetsAPIComposite(auth_composite)
        self.ports = PortsAPIComposite(auth_composite)

        self.networks.behaviors = self.networks.behavior_class(
            networks_client=self.networks.client,
            networks_config=self.networks.config,
            subnets_client=self.subnets.client,
            subnets_config=self.subnets.config,
            ports_client=self.ports.client,
            ports_config=self.ports.config)

        self.subnets.behaviors = self.subnets.behavior_class(
            subnets_client=self.subnets.client,
            subnets_config=self.subnets.config,
            networks_client=self.networks.client,
            networks_config=self.networks.config,
            ports_client=self.ports.client,
            ports_config=self.ports.config)

        self.ports.behaviors = self.ports.behavior_class(
            ports_client=self.ports.client,
            ports_config=self.ports.config,
            networks_client=self.networks.client,
            networks_config=self.networks.config,
            subnets_client=self.subnets.client,
            subnets_config=self.subnets.config)


class NetworksAdminComposite(NetworksComposite):
    _auth_composite = _NetworksAdminAuthComposite


class NetworksAPIComposite(NetworksComposite):
    behavior_class = NetworksAPIBehaviors

    def __init__(self, auth_composite):
        self.config = NetworksAPIConfig()
        self.client = NetworksClient(**auth_composite.client_args)
        self.behaviors = None


class SubnetsAPIComposite(NetworksComposite):
    behavior_class = SubnetsAPIBehaviors

    def __init__(self, auth_composite):
        self.config = SubnetsAPIConfig()
        self.client = SubnetsClient(**auth_composite.client_args)
        self.behaviors = None


class PortsAPIComposite(NetworksComposite):
    behavior_class = PortsAPIBehaviors

    def __init__(self, auth_composite):
        self.config = PortsAPIConfig()
        self.client = PortsClient(**auth_composite.client_args)
        self.behaviors = None
