"""
Copyright 2015 Rackspace

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

from cloudcafe.networking.networks.extensions.model import NeutronExtensions

content_type_fmt = '{content_type}/{content_subtype}'


class ExtensionsClient(AutoMarshallingHTTPClient):
    """
    This client will retrieve a list of Neutron extensions currently
    deployed in the target environment.

    """
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None, tenant_id=None):

        """
        @summary: Rackspace Neutron API extension client
        @param url: Base URL for the networks service
        @type url: string
        @param auth_token: Auth token to be used for all requests
        @type auth_token: string
        @param serialize_format: Format for serializing requests
        @type serialize_format: string
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: string
        @param tenant_id: optional tenant id to be included in the
            header if given
        @type tenant_id: string
        """
        super(ExtensionsClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = content_type_fmt.format(
            content_type='application',
            content_subtype=self.serialize_format)
        self.default_headers['Accept'] = content_type_fmt.format(
            content_type='application',
            content_subtype=self.deserialize_format)
        if tenant_id:
            self.default_headers['X-Auth-Project-Id'] = tenant_id
        self.url = url
        self.extensions_url = '{url}/extensions'.format(url=self.url)

    def get_deployed_extensions(self, requestslib_kwargs=None):
        """
        Get the list of extensions deployed in the target environment.
        :param requestslib_kwargs:
        :return:
        """
        return self.request('GET', self.extensions_url,
                            response_entity_type=NeutronExtensions,
                            requestslib_kwargs=requestslib_kwargs)
