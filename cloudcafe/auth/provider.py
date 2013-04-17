from cloudcafe.extensions.rax_auth.v2_0.tokens_api.client import TokenAPI_Client
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.behaviors import TokenAPI_Behaviors
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.config import TokenAPI_Config
from cloudcafe.identity.v2_0.tokens_api.client import TokenAPI_Client as OSTokenAPI_Client
from cloudcafe.identity.v2_0.tokens_api.behaviors import TokenAPI_Behaviors as OSTokenAPI_Behaviors
from cloudcafe.identity.v2_0.tokens_api.config import TokenAPI_Config as OSTokenAPI_Config

class AuthProvider(object):

    def __init__(self, auth_config):
        self.auth_config = auth_config

    def get_access_data(self):
        if self.auth_config.strategy.lower() == 'keystone':
            token_client = OSTokenAPI_Client(
                self.auth_config.authentication_endpoint, 'json', 'json')
            token_behaviors = OSTokenAPI_Behaviors(token_client)
            return token_behaviors.get_access_data(self.auth_config.username,
                                                   self.auth_config.password,
                                                   self.auth_config.tenant_name)