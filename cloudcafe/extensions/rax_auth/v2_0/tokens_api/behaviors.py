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
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.client \
    import TokenAPI_Client, MFA_TokenAPI_Client
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.config \
    import TokenAPI_Config


class TokenAPI_Behaviors(BaseBehavior):

    def __init__(self, identity_user_api_client=None):
        super(TokenAPI_Behaviors, self).__init__()
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


class MFA_TokenAPI_Behaviors(BaseBehavior):

    def __init__(self, identity_user_api_client=None):
        super(MFA_TokenAPI_Behaviors, self).__init__()
        self._client = identity_user_api_client
        self.config = TokenAPI_Config()

    @behavior(MFA_TokenAPI_Client)
    def get_access_data(self, username=None, password=None,
                        tenant_id=None, passcode=None):
        username = username or self.config.username
        password = password or self.config.password
        tenant_id = tenant_id or self.config.tenant_id
        passcode = passcode or 'bypassed_passcode'

        access_data = None
        if username is not None and password is not None:
            # Make first call to get session ID
            response = self._client.authenticate(
                username=username, password=password, tenant_id=tenant_id)
            session_id = self._get_session_id(response)

            # Make 2nd call with passcode + session ID to get token and catalog
            response = self._client.authenticate_passcode(
                session_id=session_id, passcode=passcode)
            access_data = response.entity
        return access_data

    @classmethod
    def _get_session_id(cls, response):
        """
        Finds specific response header, and parses the session id out of the
        header value

        :param response: raw request response
        :return: session_id (String)
        """

        session_header = 'www-authenticate'
        session_id = None
        if session_header in response.headers:
            session_id = response.headers[session_header].split("=")[1]
            session_id = session_id[
                         session_id.find("'") + 1: session_id.rfind("'")]
        return session_id
