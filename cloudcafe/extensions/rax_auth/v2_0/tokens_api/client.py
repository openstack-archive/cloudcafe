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

from cafe.engine.http.client import AutoMarshallingHTTPClient
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.models.requests. \
    auth import Auth as AuthRequest
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.models.responses. \
    access import Access as AuthResponse
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.models.requests. \
    credentials import ApiKeyCredentials
from cloudcafe.identity.v2_0.models import requests
from cloudcafe.extensions.rax_auth.v2_0.tokens_api.models.requests.passcode \
    import PasscodeCredentials

_version = 'v2.0'
_tokens = 'tokens'


class MFA_Session_ID_Header_Missing(Exception):
    pass


class BaseTokenAPI_Client(AutoMarshallingHTTPClient):

    def __init__(self, serialize_format, deserialize_format=None):
        super(BaseTokenAPI_Client, self).__init__(serialize_format,
                                                  deserialize_format)

    @property
    def token(self):
        return self.default_headers.get('X-Auth-Token')

    @token.setter
    def token(self, token):
        self.default_headers['X-Auth-Token'] = token

    @token.deleter
    def token(self):
        del self.default_headers['X-Auth-Token']


class TokenAPI_Client(BaseTokenAPI_Client):
    def __init__(self, url, serialize_format, deserialize_format=None,
                 auth_token=None):

        super(TokenAPI_Client, self).__init__(
            serialize_format, deserialize_format)
        self.base_url = '{0}/{1}'.format(url, _version)
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            serialize_format)

        if auth_token is not None:
            self.default_headers['X-Auth-Token'] = auth_token

    def authenticate(self, username, api_key, tenant_id,
                     requestslib_kwargs=None):

        """
        @summary: Creates authentication using Username and password.
        @param username: The username of the customer.
        @type username: String
        @param api_key: The user password.
        @type api_key: String
        @return: Response Object containing auth response
        @rtype: Response Object
        """

        credentials = ApiKeyCredentials(
            username=username,
            apiKey=api_key)
        auth_request_entity = AuthRequest(apiKeyCredentials=credentials,
                                          tenantId=tenant_id)

        url = '{0}/{1}'.format(self.base_url, _tokens)
        response = self.post(url, response_entity_type=AuthResponse,
                             request_entity=auth_request_entity,
                             requestslib_kwargs=requestslib_kwargs)
        return response


class MFA_TokenAPI_Client(BaseTokenAPI_Client):
    def __init__(self, url, serialize_format, deserialize_format=None,
                 auth_token=None):
        super(MFA_TokenAPI_Client, self).__init__(
            serialize_format, deserialize_format)
        self.base_url = '{0}/{1}'.format(url, _version)
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            serialize_format)

        if auth_token is not None:
            self.default_headers['X-Auth-Token'] = auth_token

    def authenticate(self, username, password, tenant_id, passcode,
                     requestslib_kwargs=None):
        """
        @summary: Creates authentication using Username and password.
        @param username: The username of the customer.
        @type username: String
        @param password: The user password.
        @type password: String
        @param passcode: The secondary authentication passcode
        @type password: String
        @return: Response Object containing auth response
        @rtype: Response Object
        """

        session_header = 'www-authenticate'

        request_entity = requests.Auth(
            username=username, password=password, tenant_id=tenant_id)
        url = '{0}/{1}'.format(self.base_url, _tokens)
        response = self.post(url, request_entity=request_entity,
                             requestslib_kwargs=requestslib_kwargs)

        if session_header not in response.headers:
            raise MFA_Session_ID_Header_Missing

        session_id = response.headers[session_header].split("=")[1]
        session_id = session_id[
                     session_id.find('\'') + 1: session_id.rfind('\'')]

        return self.authenticate_passcode(session_id=session_id,
                                          passcode=passcode)

    def authenticate_passcode(self, session_id, passcode,
                              requestslib_kwargs=None):
        """
        @summary: Creates authentication using username and password.
        @param session_id: The session id from the first auth stage.
        @type session_id: string
        @param passcode: The passcode that is sent to duo.
        @type passcode: string
        @return: Response Object containing auth response
        @rtype: Response Object
        """

        credentials = PasscodeCredentials(passcode=passcode)
        auth_request_entity = AuthRequest(passcodeCredentials=credentials)
        headers = {'X-SessionId': session_id}
        url = '{0}/{1}'.format(self.base_url, _tokens)
        return self.post(url, headers=headers,
                         response_entity_type=AuthResponse,
                         request_entity=auth_request_entity,
                         requestslib_kwargs=requestslib_kwargs)

