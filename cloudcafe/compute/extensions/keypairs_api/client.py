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
from cloudcafe.compute.extensions.keypairs_api.models.requests \
    import CreateKeypair
from cloudcafe.compute.extensions.keypairs_api.models.keypair \
    import Keypair, Keypairs


class KeypairsClient(AutoMarshallingRestClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        """
        @param url: Base URL for the compute service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """
        super(KeypairsClient, self).__init__(serialize_format,
                                             deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def create_keypair(self, name, public_key=None, requestslib_kwargs=None):
        request = CreateKeypair(name=name, public_key=public_key)

        url = '%s/os-keypairs' % self.url
        resp = self.request('POST', url,
                            response_entity_type=Keypair,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_keypair(self, keypair_name, requestslib_kwargs=None):

        url = '%s/os-keypairs/%s' % (self.url, keypair_name)
        resp = self.request('GET', url,
                            response_entity_type=Keypair,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_keypairs(self, requestslib_kwargs=None):

        url = '%s/os-keypairs' % self.url
        resp = self.request('GET', url,
                            response_entity_type=Keypairs,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_keypair(self, keypair_name, requestslib_kwargs=None):
        url = '%s/os-keypairs/%s' % (self.url, keypair_name)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
