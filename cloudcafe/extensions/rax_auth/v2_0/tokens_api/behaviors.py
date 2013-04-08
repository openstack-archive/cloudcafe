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
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.client import TokenAPI_Client
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.config import TokenAPI_Config


class TokenAPI_Behaviors(BaseBehavior):

    def __init__(self, identity_user_api_client=None):
        self._client = identity_user_api_client
        self.config = TokenAPI_Config()

    @behavior(TokenAPI_Client)
    def get_access_data(self, username=None, api_key=None,
                        tenant_id=None):

        username = username or self.config.username
        api_key = api_key or self.config.api_key
        tenant_id = tenant_id or self.config.tenant_id

        access_data = None
        if username is not None and api_key is not None:
            response = self._client.authenticate(
                username=username, api_key=api_key,
                tenant_id=tenant_id)
            access_data = response.entity

        return access_data
