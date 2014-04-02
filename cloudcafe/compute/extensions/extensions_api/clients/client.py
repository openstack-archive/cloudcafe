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

from cloudcafe.compute.extensions.extensions_api.models.request import \
    CreateV2BlockServer as CreateServer
from cloudcafe.compute.servers_api.models.servers import Server


class BlockV2ServersClient(AutoMarshallingHTTPClient):

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
        super(BlockV2ServersClient, self).__init__(serialize_format,
                                                   deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.serialize_format)
        accept = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def create_server(self, name, flavor_ref, block_device_mapping_v2,
                      max_count=None, min_count=None, networks=None,
                      requestslib_kwargs=None):
        """
        @summary: Creates an instance of a  block Version 2 server given the
         provided parameters
        @param name: Name of the server
        @type name: String
        @param flavor_ref: Identifier for the flavor used to build the server
        @type flavor_ref: String
        @param block_device_mapping_v2: A list of dictionaries needed for boot
         from volume V2 feature
        @type block_device_mapping: List
        @param max_count: max_count parameter for the server.
        @type max_count: String
        @param min_count: min_count parameter for the server.
        @type min_count: String
        @param networks: Networks for the server.
        @type networks: List
        @return: Response Object containing response code and
         the server domain object
        @rtype: Requests.response
        """

        server_request_object = CreateServer(
            name=name, flavor_ref=flavor_ref,
            block_device_mapping_v2=block_device_mapping_v2,
            max_count=max_count, min_count=min_count, networks=networks)

        url = '{base_url}/os-volumes_boot'.format(base_url=self.url)
        resp = self.request('POST', url,
                            response_entity_type=Server,
                            request_entity=server_request_object,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
