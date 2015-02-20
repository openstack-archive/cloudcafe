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

from cloudcafe.networking.networks.composites import _NetworkingAuthComposite
from cloudcafe.networking.networks.extensions.security_groups_api.behaviors \
    import SecurityGroupsBehaviors
from cloudcafe.networking.networks.extensions.security_groups_api.client \
    import SecurityGroupsClient
from cloudcafe.networking.networks.extensions.security_groups_api.config \
    import SecurityGroupsConfig


class SecurityGroupsComposite(object):
    networking_auth_composite = _NetworkingAuthComposite

    def __init__(self):
        auth_composite = self.networking_auth_composite()
        self.url = auth_composite.networking_url
        self.user = auth_composite._auth_user_config
        self.config = SecurityGroupsConfig()
        self.client = SecurityGroupsClient(**auth_composite.client_args)

        self.behaviors = SecurityGroupsBehaviors(
            security_groups_client=self.client,
            security_groups_config=self.config)
