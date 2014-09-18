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
        @param name: human readable name for the network,
            may not be unique. (CRUD: CRU)
        @type name: string
        @param admin_state_up: true or false, the admin state
            of the network. If down, the network does not forward packets.
            Default value is True (CRUD: CRU)
        @type admin_state_up: bool
        @param shared: specifies if the network can be accessed by any
            tenant. Default value is False. (CRUD: CRU)
        @type shared: bool
        @param tenant_id: owner of the network. (CRUD: CR)
        @type tenant_id: string
        @return: network create response
        @rtype: Requests.response
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
        @param network_id: The UUID for the network
        @type network_id: string
        @param name: human readable name for the network, may not be unique.
            (CRUD: CRU)
        @type name: string
        @param admin_state_up: true or false, the admin state of the network.
            If down, the network does not forward packets. Default value is
            True (CRUD: CRU)
        @type admin_state_up: bool
        @param shared: specifies if the network can be accessed by any tenant.
            Default value is False. (CRUD: CRU)
        @type shared: bool
        @param tenant_id: owner of the network. (CRUD: CR)
        @type tenant_id: string
        @return: update network response
        @rtype: Requests.response
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
        @param network_id: The UUID for the network
        @type network_id: string
        @return: get network response
        @rtype: Requests.response
        """

        url = '{base_url}/networks/{network_id}'.format(
            base_url=self.url, network_id=network_id)
        resp = self.request('GET', url,
                            response_entity_type=Network,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_networks(self, network_id=None, name=None, status=None,
                      admin_state_up=None, shared=None, tenant_id=None,
                      limit=None, marker=None, page_reverse=None,
                      requestslib_kwargs=None):
        """
        @summary: Lists networks, filtered by params if given
        @param network_id: network ID to filter by
        @type network_id: string
        @param name: network name to filter by
        @type name: string
        @param status: network status to filter by
        @type status: string
        @param admin_state_up: Admin state of the network to filter by
        @type admin_state_up: bool
        @param shared: If network is shared across tenants status to filter by
        @type shared: bool
        @param tenant_id: tenant ID network owner to filter by
        @type tenant_id: string
        @param limit: page size
        @type limit: int
        @param marker: Id of the last item of the previous page
        @type marker: string
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @return: list networks response
        @rtype: Requests.response
        """

        params = {'id': network_id, 'name': name, 'status': status,
                  'admin_state_up': admin_state_up, 'shared': shared,
                  'tenant_id': tenant_id, 'limit': limit, 'marker': marker,
                  'page_reverse': page_reverse}
        url = '{base_url}/networks'.format(base_url=self.url)
        resp = self.request('GET', url, params=params,
                            response_entity_type=Networks,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_network(self, network_id, requestslib_kwargs=None):
        """
        @summary: Deletes a specified network and its associated resources
        @param network_id: The UUID for the network
        @type network_id: string
        @return: delete network response
        @rtype: Requests.response
        """

        url = '{base_url}/networks/{network_id}'.format(
            base_url=self.url, network_id=network_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
