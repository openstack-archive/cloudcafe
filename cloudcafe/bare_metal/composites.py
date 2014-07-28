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
from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.bare_metal.chassis.composites import ChassisComposite
from cloudcafe.bare_metal.config import MarshallingConfig, \
    BareMetalEndpointConfig
from cloudcafe.bare_metal.drivers.composites import DriversComposite
from cloudcafe.bare_metal.nodes.composites import NodesComposite
from cloudcafe.bare_metal.ports.composites import PortsComposite


class _BareMetalAuthComposite(MemoizedAuthServiceComposite):
    _auth_endpoint_config = UserAuthConfig
    _auth_user_config = UserConfig
    _bare_metal_endpoint_config = BareMetalEndpointConfig

    def __init__(self):
        self.metal_endpoint_config = self._bare_metal_endpoint_config()
        self.marshalling_config = MarshallingConfig()

        super(_BareMetalAuthComposite, self).__init__(
            service_name=self.metal_endpoint_config.bare_metal_endpoint_name,
            region=self.metal_endpoint_config.region,
            endpoint_config=self._auth_endpoint_config(),
            user_config=self._auth_user_config())

        self.bare_metal_url = self.public_url

        if self.metal_endpoint_config.bare_metal_endpoint_url:
            self.bare_metal_url = '{0}/{1}'.format(
                self.metal_endpoint_config.bare_metal_endpoint_url,
                self.tenant_id)

        self.client_args = {
            'url': self.bare_metal_url,
            'auth_token': self.token_id,
            'serialize_format': self.marshalling_config.serializer,
            'deserialize_format': self.marshalling_config.deserializer}


class BareMetalComposite(object):
    _auth_composite = _BareMetalAuthComposite

    def __init__(self):
        auth_composite = self._auth_composite()
        self.user = auth_composite._auth_user_config
        self.chassis = ChassisComposite(auth_composite)
        self.nodes = NodesComposite(auth_composite)
        self.drivers = DriversComposite(auth_composite)
        self.ports = PortsComposite(auth_composite)
