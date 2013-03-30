"""
Copyright 2013 Rackspace

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

from cafe.engine.behaviors import BaseBehavior, behavior
from cloudcafe.identity.v2_0.tokens_api.client import TokenAPI_Client
from cloudcafe.identity.v2_0.tokens_api.config import TokenAPI_Config


class TokenAPI_Behaviors(BaseBehavior):

    def __init__(self, identity_user_api_client=None):
        self._client = identity_user_api_client
        self.config = TokenAPI_Config()

    @behavior(TokenAPI_Client)
    def get_access_data(self, username=None, password=None,
                        tenant_name=None):

        username = username or self.config.username
        password = password or self.config.password
        tenant_name = tenant_name or self.config.tenant_name

        access_data = None
        if username is not None and password is not None:
            response = self._client.authenticate(
                username=username, password=password,
                tenant_name=tenant_name)
            access_data = response.entity

        return access_data
