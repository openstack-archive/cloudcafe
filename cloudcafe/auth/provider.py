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
    TokenAPI_Client as RaxTokenAPI_Client, \
    MFA_TokenAPI_Client as RaxToken_MFA_API_Client

from cloudcafe.extensions.rax_auth.v2_0.tokens_api.behaviors \
    import TokenAPI_Behaviors as RaxTokenAPI_Behaviors, \
    MFA_TokenAPI_Behaviors as RaxToken_MFA_API_Behaviors

from cloudcafe.extensions.saio_tempauth.v1_0.client import \
    TempauthAPI_Client as SaioAuthAPI_Client
from cloudcafe.extensions.saio_tempauth.v1_0.behaviors import \
    TempauthAPI_Behaviors as SaioAuthAPI_Behaviors
from cloudcafe.identity.v2_0.behaviors import IdentityServiceBehaviors


class MemoizedAuthServiceCompositeException(Exception):
    pass


class MemoizedAuthServiceComposite(object):

    def __init__(
            self, service_name, region, endpoint_config=None,
            user_config=None):

        self.endpoint_config = endpoint_config or UserAuthConfig()
        self.user_config = user_config or UserConfig()
        self.service_name = service_name
        self.region = region

    @classmethod
    @memoized
    def get_rackspace_access_data(
            cls, username, api_key, tenant_id, auth_endpoint):
        client = RaxTokenAPI_Client(auth_endpoint, 'json', 'json')
        behaviors = RaxTokenAPI_Behaviors(client)
        return behaviors.get_access_data(username, api_key, tenant_id)

    @classmethod
    @memoized
    def get_rackspace_mfa_access_data(
            cls, username, password, tenant_id, auth_endpoint, passcode):
        if passcode is None:
            # TODO: This is a place holder for adding the functionality to
            # use an external service (e.g. - SMS) to provide the passcode
            # Also add this to get_access_data() in the AuthProvider class
            pass
        token_client = RaxToken_MFA_API_Client(
            url=auth_endpoint, serialize_format='json',
            deserialize_format='json')
        token_behaviors = RaxToken_MFA_API_Behaviors(token_client)
        return token_behaviors.get_access_data(
            username=username, password=password, tenant_id=tenant_id)

    @classmethod
    @memoized
    def get_keystone_access_data(
            cls, username, password, tenant_name, auth_endpoint):
        return IdentityServiceBehaviors.get_access_data(
            username, password, tenant_name, auth_endpoint)

    @classmethod
    @memoized
    def get_saio_tempauth_access_data(
            cls, username, password, auth_endpoint):
        client = SaioAuthAPI_Client(auth_endpoint)
        behaviors = SaioAuthAPI_Behaviors(client)
        return behaviors.get_access_data(username, password)

    @property
    def access_data(self):
        if self.auth_strategy == 'keystone':
            return self.get_keystone_access_data(
                self.user_config.username, self.user_config.password,
                self.user_config.tenant_name,
                self.endpoint_config.auth_endpoint)

        elif self.auth_strategy == 'rax_auth':
            return self.get_rackspace_access_data(
                self.user_config.username, self.user_config.api_key,
                self.user_config.tenant_id, self.endpoint_config.auth_endpoint)

        elif self.auth_strategy == 'rax_auth_mfa':
            return self.get_rackspace_mfa_access_data(
                self.user_config.username, self.user_config.password,
                self.user_config.tenant_id, self.endpoint_config.auth_endpoint,
                self.user_config.passcode)

        elif self.auth_strategy == 'saio_tempauth':
            return self.get_saio_tempauth_access_data(
                self.user_config.username, self.user_config.password,
                self.endpoint_config.auth_endpoint)
        else:
            raise NotImplementedError

    @property
    def auth_strategy(self):
        return self.endpoint_config.strategy.lower()

    @property
    def token_id(self):
        return self.access_data.token.id_

    @property
    def tenant_id(self):
        return self.access_data.token.tenant.id_

    @property
    def public_url(self):
        endpoint = self.service.get_endpoint(self.region)
        try:
            return endpoint.public_url
        except AttributeError:
            raise MemoizedAuthServiceCompositeException(
                "Unable to locate an endpoint with the region '{0}' in the "
                "service '{1}' from the service service catalog for user {2}. "
                "No public URL found.".format(
                    self.region, self.service_name, self.tenant_id))

    @property
    def service(self):
        service = self.access_data.get_service(self.service_name)
        if not service:
            raise MemoizedAuthServiceCompositeException(
                "Unable to locate a service named '{0}' in the service catalog"
                " for the user {1}".format(self.service_name, self.tenant_id))
        return service


class AuthProvider(object):

    @staticmethod
    def get_access_data(endpoint_config=None, user_config=None):
        endpoint_config = endpoint_config or UserAuthConfig()
        user_config = user_config or UserConfig()

        if endpoint_config.strategy.lower() == 'keystone':
            return IdentityServiceBehaviors.get_access_data(
                user_config.username, user_config.password,
                user_config.tenant_name, endpoint_config.auth_endpoint)

        elif endpoint_config.strategy.lower() == 'rax_auth':
            token_client = RaxTokenAPI_Client(
                endpoint_config.auth_endpoint, 'json', 'json')
            token_behaviors = RaxTokenAPI_Behaviors(token_client)
            return token_behaviors.get_access_data(user_config.username,
                                                   user_config.api_key,
                                                   user_config.tenant_id)

        elif endpoint_config.strategy.lower() == 'rax_auth_mfa':
            passcode = user_config.passcode
            if passcode is None:
                # TODO: This is a place holder for adding the functionality to
                # use an external service (e.g. - SMS) to provide the passcode
                pass
            token_client = RaxToken_MFA_API_Client(
                url=endpoint_config.auth_endpoint,
                serialize_format='json', deserialize_format='json')
            token_behaviors = RaxToken_MFA_API_Behaviors(token_client)
            return token_behaviors.get_access_data(
                username=user_config.username, password=user_config.password,
                tenant_id=user_config.tenant_id, passcode=passcode)

        elif endpoint_config.strategy.lower() == 'saio_tempauth':
            auth_client = SaioAuthAPI_Client(endpoint_config.auth_endpoint)
            auth_behaviors = SaioAuthAPI_Behaviors(auth_client)
            return auth_behaviors.get_access_data(
                user_config.username, user_config.password)

        else:
            raise NotImplementedError
