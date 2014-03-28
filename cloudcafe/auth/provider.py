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
from cafe.drivers.unittest.decorators import memoized
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


class MemoizedAuthServiceComposite(object):

    class _lazy_property(object):
        '''
        meant to be used for lazy evaluation of an object attribute.
        property should represent non-mutable data, as it replaces itself.
        '''

        def __init__(self, func):
            self.func = func
            self.func_name = func.__name__

        def __get__(self, obj, cls):
            if obj is None:
                return None
            value = self.func(obj)
            setattr(obj, self.func_name, value)
            return value

    def __init__(
            self, service_name, region, endpoint_config=None,
            user_config=None):

        self.endpoint_config = endpoint_config or UserAuthConfig()
        self.user_config = user_config or UserConfig()
        self.access_data = self.cache_access_data()
        self.token_id = self.access_data.token.id_
        self.tenant_id = self.access_data.token.tenant.id_
        self.service_name = service_name
        self.region = region

    @classmethod
    @memoized
    def cache_access_data(cls, endpoint_config=None, user_config=None):
        access_data = AuthProvider.get_access_data(
            endpoint_config, user_config)
        if access_data is None:
            raise AssertionError('Authentication failed in setup')
        cls.access_data = access_data
        return cls.access_data

    @_lazy_property
    def public_url(self):
        endpoint = self.service.get_endpoint(self.region)
        return endpoint.public_url

    @_lazy_property
    def service(self):
        return self.access_data.get_service(self.service_name)


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
