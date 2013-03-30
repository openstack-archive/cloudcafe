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

from cafe.engine.clients.rest import AutoMarshallingRestClient

from cloudcafe.identity.v2_0.tokens_api.models.requests.auth import \
    Auth as AuthRequest
from cloudcafe.identity.v2_0.tokens_api.models.responses.access import \
    Access as AuthResponse
from cloudcafe.identity.v2_0.tokens_api.models.requests.credentials import \
    PasswordCredentials

_version = 'v2.0'
_tokens = 'tokens'


class BaseTokenAPI_Client(AutoMarshallingRestClient):

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

    def authenticate(self, username, password, tenant_name,
                     requestslib_kwargs=None):

        '''
        @summary: Creates authentication using Username and password.
        @param username: The username of the customer.
        @type name: String
        @param password: The user password.
        @type password: String
        @return: Response Object containing auth response
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/tokens
        '''
        credentials = PasswordCredentials(
            username=username,
            password=password)
        auth_request_entity = AuthRequest(credentials=credentials,
                                          tenant_name=tenant_name)

        url = '{0}/{1}'.format(self.base_url, _tokens)
        response = self.post(url, response_entity_type=AuthResponse,
                             request_entity=auth_request_entity,
                             requestslib_kwargs=requestslib_kwargs)
        return response
