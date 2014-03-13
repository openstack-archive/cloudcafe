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

from cloudcafe.designate.client import DesignateClient
from cloudcafe.designate.v1.server_api.models.requests import ServerRequest
from cloudcafe.designate.v1.server_api.models.responses import \
    ServerResponse, ServerListResponse


class ServerAPIClient(DesignateClient):

    def __init__(self, url, serialize_format=None,
                 deserialize_format=None):
        super(ServerAPIClient, self).__init__(url, serialize_format,
                                              deserialize_format)

    def _get_servers_url(self):
        return "{0}/servers".format(self.url)

    def _get_server_url(self, server_id):
        return "{0}/{1}".format(self._get_servers_url(), server_id)

    def create_server(self, name=None, **requestslib_kwargs):
        """POST /servers"""
        server = ServerRequest(name=name)
        url = self._get_servers_url()
        return self.request('POST', url, response_entity_type=ServerResponse,
                            request_entity=server,
                            requestslib_kwargs=requestslib_kwargs)

    def update_server(self, server_id, name, **requestslib_kwargs):
        """PUT /servers/{serverID}"""
        server = ServerRequest(name=name)
        url = self._get_server_url(server_id)
        return self.request('PUT', url, response_entity_type=ServerResponse,
                            request_entity=server,
                            requestslib_kwargs=requestslib_kwargs)

    def list_servers(self, **requestslib_kwargs):
        """GET /servers"""
        url = self._get_servers_url()
        return self.request('GET', url,
                            response_entity_type=ServerListResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def get_server(self, server_id, **requestslib_kwargs):
        """GET /servers/{serverID}"""
        url = self._get_server_url(server_id)
        return self.request('GET', url, response_entity_type=ServerResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_server(self, server_id, **requestslib_kwargs):
        """DELETE /servers/{serverID}"""
        url = self._get_server_url(server_id)
        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
