"""
Copyright 2015 Rackspace

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

from cloudcafe.networking.networks.composites import _NetworkingAuthComposite
from cloudcafe.networking.networks.extensions.ip_addresses_api.behaviors \
    import IPAddressesBehaviors
from cloudcafe.networking.networks.extensions.ip_addresses_api.client \
    import IPAddressesClient
from cloudcafe.networking.networks.extensions.ip_addresses_api.config \
    import IPAddressesConfig


class IPAddressesComposite(object):
    networking_auth_composite = _NetworkingAuthComposite

    def __init__(self):
        auth_composite = self.networking_auth_composite()
        self.url = auth_composite.networking_url
        self.user = auth_composite._auth_user_config
        self.config = IPAddressesConfig()
        self.client = IPAddressesClient(**auth_composite.client_args)

        self.behaviors = IPAddressesBehaviors(
            ip_addresses_client=self.client,
            ip_addresses_config=self.config)
