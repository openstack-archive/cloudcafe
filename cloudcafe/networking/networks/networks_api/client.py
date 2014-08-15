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
from cloudcafe.networking.networks.common.models.request.network \
    import NetworkRequest
from cloudcafe.networking.networks.common.models.response.network \
    import Network, Networks


class NetworksClient(AutoMarshallingHTTPClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None, tenant_id=None):
        """
        @param string url: Base URL for the networks service
        @param string auth_token: Auth token to be used for all requests
        @param string serialize_format: Format for serializing requests
        @param string deserialize_format: Format for de-serializing responses
        @param string tenant_id: optional tenant id to be included in the
            header if given
        """
        super(NetworksClient, self).__init__(serialize_format,
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
        if tenant_id:
            self.default_headers['X-Auth-Project-Id'] = tenant_id
        self.url = url

    def create_network(self, name=None, admin_state_up=None, shared=None,
                       tenant_id=None, requestslib_kwargs=None):
        """
        @summary: Creates a Network
        @param string name: human readable name for the network,
            may not be unique. (CRUD: CRU)
        @param bool admin_state_up: true or false, the admin state
            of the network. If down, the network does not forward packets.
            Default value is True (CRUD: CRU)
        @param bool shared: specifies if the network can be accessed by any
            tenant. Default value is False. (CRUD: CRU)
        @param string tenant_id: owner of the network. (CRUD: CR)
        """
        url = '{base_url}/networks'.format(base_url=self.url)

        request = NetworkRequest(name=name, admin_state_up=admin_state_up,
                                 shared=shared, tenant_id=tenant_id)

        resp = self.request('POST', url,
                            response_entity_type=Network,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def update_network(self, network_id, name=None, admin_state_up=None,
                       shared=None, tenant_id=None, requestslib_kwargs=None):
        """
        @summary: Updates a specified Network
        @param string network_id: The UUID for the network
        @param string name: human readable name for the network,
            may not be unique. (CRUD: CRU)
        @param bool admin_state_up: true or false, the admin state
            of the network. If down, the network does not forward packets.
            Default value is True (CRUD: CRU)
        @param bool shared: specifies if the network can be accessed by any
            tenant. Default value is False. (CRUD: CRU)
        @param string tenant_id: owner of the network. (CRUD: CR)
        """

        url = '{base_url}/networks/{network_id}'.format(
            base_url=self.url, network_id=network_id)

        request = NetworkRequest(name=name, admin_state_up=admin_state_up,
                                 shared=shared, tenant_id=tenant_id)
        resp = self.request('PUT', url,
                            response_entity_type=Network,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_network(self, network_id, requestslib_kwargs=None):
        """
        @summary: Shows information for a specified network
        @param string network_id: The UUID for the network
        """

        url = '{base_url}/networks/{network_id}'.format(
            base_url=self.url, network_id=network_id)
        resp = self.request('GET', url,
                            response_entity_type=Network,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_networks(self, requestslib_kwargs=None):
        """
        @summary: Lists networks
        """

        # TODO: add field query params to filter the response
        url = '{base_url}/networks'.format(base_url=self.url)
        resp = self.request('GET', url,
                            response_entity_type=Networks,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_network(self, network_id, requestslib_kwargs=None):
        """
        @summary: Deletes a specified network and its associated resources
        @param string network_id: The UUID for the network
        """

        url = '{base_url}/networks/{network_id}'.format(
            base_url=self.url, network_id=network_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
