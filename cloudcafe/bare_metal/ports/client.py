"""
Copyright 2014 Rackspace

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

from cloudcafe.bare_metal.ports.models.responses import Port, Ports
from cloudcafe.bare_metal.ports.models.requests import CreatePort


class PortsClient(AutoMarshallingHTTPClient):

    def __init__(
            self, url, auth_token, serialize_format=None,
            deserialize_format=None):

        super(PortsClient, self).__init__(
            serialize_format, deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)

    def list_ports(self, requestslib_kwargs=None):
        """
        @summary: Lists all ports with details.
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/ports'.format(base_url=self.url)
        resp = self.get(url, response_entity_type=Ports,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_port(self, uuid, requestslib_kwargs=None):
        """
        @summary: Retrieves the details of an individual port.
        @param uuid: The uuid of an existing port
        @type uuid: String
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/ports/{uuid}'.format(
            base_url=self.url, uuid=uuid)
        resp = self.get(url, response_entity_type=Port,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def create_port(
            self, node_uuid=None, address=None, extra=None,
            requestslib_kwargs=None):
        """
        @summary: Creates a port from the provided parameters.
        @param node_uuid: The node the port is associated with
        @type node_uuid: String
        @param address: The MAC address of the port
        @type address: String
        @param extra: Extra metadata for the node
        @type extra: Dict
        @return: resp
        @rtype: Requests.response
        """
        request = CreatePort(
            node_uuid=node_uuid, address=address, extra=extra)

        url = '{base_url}/ports'.format(base_url=self.url)
        resp = self.post(url,
                         response_entity_type=Port,
                         request_entity=request,
                         requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_port(self, uuid, requestslib_kwargs=None):
        """
        @summary: Deletes the specified port.
        @param uuid: The uuid of a port
        @type uuid: String
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/ports/{uuid}'.format(
            base_url=self.url, uuid=uuid)
        resp = self.delete(url, requestslib_kwargs=requestslib_kwargs)
        return resp
