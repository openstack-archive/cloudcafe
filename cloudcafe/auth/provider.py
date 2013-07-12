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
from cloudcafe.auth.config import UserAuthConfig, UserConfig
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.client import \
    TokenAPI_Client as RaxTokenAPI_Client
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.behaviors import \
    TokenAPI_Behaviors as RaxTokenAPI_Behaviors
from cloudcafe.extensions.saio_tempauth.v1_0.client import \
    TempauthAPI_Client as SaioAuthAPI_Client
from cloudcafe.extensions.saio_tempauth.v1_0.behaviors import \
    TempauthAPI_Behaviors as SaioAuthAPI_Behaviors
from cloudcafe.identity.v2_0.tokens_api.client import \
    TokenAPI_Client as OSTokenAPI_Client
from cloudcafe.identity.v2_0.tokens_api.behaviors import \
    TokenAPI_Behaviors as OSTokenAPI_Behaviors


class AuthProvider(object):

    @staticmethod
    def get_access_data(endpoint_config=None, user_config=None):
        endpoint_config = endpoint_config or UserAuthConfig()
        user_config = user_config or UserConfig()

        if endpoint_config.strategy.lower() == 'keystone':
            token_client = OSTokenAPI_Client(
                endpoint_config.auth_endpoint, 'json', 'json')
            token_behaviors = OSTokenAPI_Behaviors(token_client)
            return token_behaviors.get_access_data(user_config.username,
                                                   user_config.password,
                                                   user_config.tenant_name)

        elif endpoint_config.strategy.lower() == 'rax_auth':
            token_client = RaxTokenAPI_Client(
                endpoint_config.auth_endpoint, 'json', 'json')
            token_behaviors = RaxTokenAPI_Behaviors(token_client)
            return token_behaviors.get_access_data(user_config.username,
                                                   user_config.api_key,
                                                   user_config.tenant_id)

        elif endpoint_config.strategy.lower() == 'saio_tempauth':
            auth_client = SaioAuthAPI_Client(endpoint_config.auth_endpoint)
            auth_behaviors = SaioAuthAPI_Behaviors(auth_client)
            return auth_behaviors.get_access_data(
                user_config.username, user_config.password)

        else:
            raise NotImplementedError
