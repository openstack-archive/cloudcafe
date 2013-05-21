from cloudcafe.extensions.rax_auth.v2_0.tokens_api.client import \
    TokenAPI_Client as RaxTokenAPI_Client
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.behaviors import \
    TokenAPI_Behaviors as RaxTokenAPI_Behaviors
from cloudcafe.identity.v2_0.tokens_api.client import \
    TokenAPI_Client as OSTokenAPI_Client
from cloudcafe.identity.v2_0.tokens_api.behaviors import \
    TokenAPI_Behaviors as OSTokenAPI_Behaviors
from cloudcafe.auth.config import UserAuthConfig, UserConfig


class AuthProvider(object):
    @classmethod
    def get_access_data(self, endpoint_config=None, user_config=None):
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
        else:
            raise NotImplementedError
