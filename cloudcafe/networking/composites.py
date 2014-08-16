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

from cloudcafe.auth.config import UserAuthConfig, UserConfig,\
    NetworkingAdminAuthConfig, NetworkingAdminUserConfig
from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.compute.config import MarshallingConfig
from cloudcafe.networking.config import NetworkingEndpointConfig,\
    NetworkingAdminEndpointConfig
from cloudcafe.networking.nets_subnets_ports_api.composites import\
    NetsSubnetsPortsComposite


class _NetworkingAuthComposite(MemoizedAuthServiceComposite):
    _networking_endpoint_config = NetworkingEndpointConfig
    _auth_endpoint_config = UserAuthConfig
    _auth_user_config = UserConfig

    def __init__(self):
        self.networking_endpoint_config = self._networking_endpoint_config()
        self.marshalling_config = MarshallingConfig()
        self._auth_endpoint_config = self._auth_endpoint_config()
        self._auth_user_config = self._auth_user_config()

        super(_NetworkingAuthComposite, self).__init__(
            service_name=(
                self.networking_endpoint_config.networking_endpoint_name),
            region=self.networking_endpoint_config.region,
            endpoint_config=self._auth_endpoint_config,
            user_config=self._auth_user_config)

        self.networking_url = self.public_url

        if self.networking_endpoint_config.networking_endpoint_url:
            self.networking_url = (
                self.networking_endpoint_config.networking_endpoint_url)

        self.client_args = {
            'url': self.networking_url,
            'auth_token': self.token_id,
            'serialize_format': self.marshalling_config.serializer,
            'deserialize_format': self.marshalling_config.deserializer}


class _NetworkingAdminAuthComposite(_NetworkingAuthComposite):
    _networking_endpoint_config = NetworkingAdminEndpointConfig
    _auth_endpoint_config = NetworkingAdminAuthConfig
    _auth_user_config = NetworkingAdminUserConfig


class NetworkingComposite(object):
    _auth_composite = _NetworkingAuthComposite

    def __init__(self):
        auth_composite = self._auth_composite()
        self.nets_subnets_ports = NetsSubnetsPortsComposite(auth_composite)


class NetworkingAdminComposite(NetworkingComposite):
    _auth_composite = _NetworkingAdminAuthComposite
