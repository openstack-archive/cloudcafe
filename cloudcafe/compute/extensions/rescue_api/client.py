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
from cloudcafe.compute.servers_api.models.servers import Server
from cloudcafe.compute.extensions.rescue_api.models.requests import \
    RescueMode, ExitRescueMode
from cloudcafe.compute.extensions.rescue_api.models.responses import \
    RescueResponse


class RescueClient(AutoMarshallingRestClient):

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
        super(RescueClient, self).__init__(serialize_format,
                                           deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def rescue(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request(
            'POST', url, response_entity_type=RescueResponse,
            request_entity=RescueMode(),
            requestslib_kwargs=requestslib_kwargs)
        return resp

    def unrescue(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request(
            'POST', url, response_entity_type=Server,
            request_entity=ExitRescueMode(),
            requestslib_kwargs=requestslib_kwargs)
        return resp
