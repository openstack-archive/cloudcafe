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
from cloudcafe.networking.networks.common.config import NetworkingBaseConfig
from cloudcafe.networking.networks.config import MarshallingConfig,\
    NetworkingEndpointConfig, NetworkingAdminEndpointConfig,\
    NetworkingAdminAuthConfig, NetworkingSecondUserConfig, \
    NetworkingAdminUserConfig, UserAuthConfig, UserConfig
from cloudcafe.networking.networks.behaviors import NetworkingBehaviors
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.networks_api.client import NetworksClient
from cloudcafe.networking.networks.networks_api.config import NetworksConfig
from cloudcafe.networking.networks.networks_api.behaviors \
    import NetworksBehaviors
from cloudcafe.networking.networks.ports_api.client import PortsClient
from cloudcafe.networking.networks.ports_api.config import PortsConfig
from cloudcafe.networking.networks.ports_api.behaviors import PortsBehaviors
from cloudcafe.networking.networks.subnets_api.client import SubnetsClient
from cloudcafe.networking.networks.subnets_api.config import SubnetsConfig
from cloudcafe.networking.networks.subnets_api.behaviors \
    import SubnetsBehaviors


class _NetworkingAuthComposite(MemoizedAuthServiceComposite):
    _networking_config = NetworkingBaseConfig
    _networking_endpoint_config = NetworkingEndpointConfig
    _auth_endpoint_config = UserAuthConfig
    _auth_user_config = UserConfig

    def __init__(self):
        self.networking_endpoint_config = self._networking_endpoint_config()
        self.marshalling_config = MarshallingConfig()
        self._auth_endpoint_config = self._auth_endpoint_config()
        self._auth_user_config = self._auth_user_config()

        super(_NetworkingAuthComposite, self).__init__(
            service_name=self.networking_endpoint_config.\
                networking_endpoint_name,
            region=self.networking_endpoint_config.region,
            endpoint_config=self._auth_endpoint_config,
            user_config=self._auth_user_config)

        self.networking_url = self.public_url

        # Overriding the publicURL if networking_endpoint_url given
        if self.networking_endpoint_config.networking_endpoint_url:
            self.networking_url = \
                self.networking_endpoint_config.networking_endpoint_url

        # Ending backslash is not expected, removing if present
        if self.networking_url[-1] == '/':
            self.networking_url = self.networking_url[:-1]

        self.client_args = {
            'url': self.networking_url,
            'auth_token': self.token_id,
            'serialize_format': self.marshalling_config.serializer,
            'deserialize_format': self.marshalling_config.deserializer}

        if self.networking_endpoint_config.header_tenant_id:
            self.client_args.update(
                tenant_id=self.networking_endpoint_config.header_tenant_id)


class _NetworkingAdminAuthComposite(_NetworkingAuthComposite):
    _networking_endpoint_config = NetworkingAdminEndpointConfig
    _auth_endpoint_config = NetworkingAdminAuthConfig
    _auth_user_config = NetworkingAdminUserConfig


class NetworkingComposite(object):
    networking_auth_composite = _NetworkingAuthComposite
    behavior_class = NetworkingBehaviors

    def __init__(self):
        auth_composite = self.networking_auth_composite()
        self.url = auth_composite.networking_url
        self.user = auth_composite._auth_user_config
        self.config = NetworkingBaseConfig()
        self.networks = NetworksComposite(auth_composite)
        self.subnets = SubnetsComposite(auth_composite)
        self.ports = PortsComposite(auth_composite)
        self.common = NetworkingCommonComposite()

        # Parent behavior can be used directly with parent config values
        self.common.behaviors = self.common.behavior_class(
            networks_client=self.networks.client,
            networks_config=self.networks.config,
            subnets_client=self.subnets.client,
            subnets_config=self.subnets.config,
            ports_client=self.ports.client,
            ports_config=self.ports.config)

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

        # Integrates all behaviors for helper methods
        self.behaviors = NetworkingBehaviors(
            networks_behaviors=self.networks.behaviors,
            subnets_behaviors=self.subnets.behaviors,
            ports_behaviors=self.ports.behaviors)


class NetworkingAdminComposite(NetworkingComposite):
    _auth_composite = _NetworkingAdminAuthComposite


class NetworkingCommonComposite(object):
    behavior_class = NetworkingBaseBehaviors

    def __init__(self):
        self.behaviors = None


class NetworksComposite(object):
    behavior_class = NetworksBehaviors

    def __init__(self, auth_composite):
        self.config = NetworksConfig()
        self.client = NetworksClient(**auth_composite.client_args)
        self.behaviors = None


class SubnetsComposite(object):
    behavior_class = SubnetsBehaviors

    def __init__(self, auth_composite):
        self.config = SubnetsConfig()
        self.client = SubnetsClient(**auth_composite.client_args)
        self.behaviors = None


class PortsComposite(object):
    behavior_class = PortsBehaviors

    def __init__(self, auth_composite):
        self.config = PortsConfig()
        self.client = PortsClient(**auth_composite.client_args)
        self.behaviors = None
