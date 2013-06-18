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
from cloudcafe.identity.config import IdentityExtensionConfig
from cloudcafe.identity.v2_0.extensions_api.models.responses.extensions \
    import Extensions
from cloudcafe.identity.v2_0.tenants_api.models.responses.role import Roles

_version = 'v2.0'


class ExtensionsAPI_Client(AutoMarshallingRestClient):
    def __init__(self, url=None, auth_token=None,
                 serialized_format=None, deserialized_format=None,
                 extensions_admin=None):
        """
        @param url: Base URL for the compute service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialized_format: Format for serializing requests
        @type serialized_format: String
        @param deserialized_format: Format for de-serializing responses
        @type deserialized_format: String
        """
        super(ExtensionsAPI_Client, self).__init__(
            serialized_format, deserialized_format)
        self.base_url = '{0}/{1}'.format(url, _version)
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            serialized_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            serialized_format)
        self.default_headers['X-Auth-Token'] = auth_token
        self.extensions_admin = extensions_admin or \
            IdentityExtensionConfig().extensions_api_admin

    def list_extensions(self, requestslib_kwards=None):
        """
        @summary: Lists all the extensions. Maps to /extensions
        @return: server_response
        @rtype: Response
        """
        url = '{0}/extensions'.format(self.base_url)
        server_response = self.request('GET', url,
                                       response_entity_type=Extensions,
                                       requestslib_kwargs=requestslib_kwards)

        return server_response

    def list_roles(self, requestslib_kwards=None):
        """
        @summary: List all roles.
        @return: response
        @rtype: Response
        """
        url = '{0}/{1}/roles'.format(self.base_url, self.extensions_admin)
        response = self.request('GET', url,
                                response_entity_type=Roles,
                                requestslib_kwargs=requestslib_kwards)

        return response
