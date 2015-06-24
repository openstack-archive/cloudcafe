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
from cloudcafe.networking.networks.extensions.ip_addresses_api.models.request\
    import IPAddressRequest
from cloudcafe.networking.networks.extensions.ip_addresses_api.models.response\
    import IPAddress, IPAddresses


class IPAddressesClient(AutoMarshallingHTTPClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None, tenant_id=None):
        """
        @summary: Rackspace Neutron API IP Addresses extension client
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
        super(IPAddressesClient, self).__init__(serialize_format,
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
        self.ip_addresses_url = '{url}/ip_addresses'.format(url=self.url)

    def create_ip_address(self, network_id=None, version=None, device_ids=None,
                          port_ids=None, requestslib_kwargs=None):
        """
        @summary: Creates an IP address on a specified network
            A list of device_ids may be optionally specified to create the IP
            address and added to their respective ports. A list of port_ids may
            be optionally specified to create the IP address and added to the
            specified ports. At least one of device_ids or port_ids must be
            specified.
        @param network_id: network UUID to get the IP address from
        @type network_id: str
        @param version: IP address version 4 or 6
        @type version: int
        @param device_ids (optional): server UUIDs to add the IP address to
            their respective ports on the given network
        @type device_ids: list
        @param port_ids(optional): port UUIDs to add the IP address on the
            given network
        @type port_ids: list
        @return: IP address create response
        @rtype: Requests.response
        """
        url = self.ip_addresses_url
        request = IPAddressRequest(network_id=network_id, version=version,
                                   device_ids=device_ids, port_ids=port_ids)

        resp = self.request('POST', url,
                            response_entity_type=IPAddress,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def update_ip_address(self, ip_address_id, port_ids=None,
                          requestslib_kwargs=None):
        """
        @summary: Update an IP address, ex. to change ports.
            This will eliminate any previous associations to ports.
        @param ip_address_id: The UUID for the ip_address
        @type ip_address_id: str
        @param port_ids: port UUIDs to associate to the IP address
        @return: IP address update response
        @rtype: Requests.response
        """
        url = '{base_url}/{ip_address_id}'.format(
            base_url=self.ip_addresses_url, ip_address_id=ip_address_id)
        request = IPAddressRequest(port_ids=port_ids)

        resp = self.request('PUT', url,
                            response_entity_type=IPAddress,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_ip_address(self, ip_address_id, requestslib_kwargs=None):
        """
        @summary: Shows a specific IP address
        @param ip_address_id: The UUID for the ip_address
        @type ip_address_id: str
        @return: IP address get response
        @rtype: Requests.response
        """
        url = '{base_url}/{ip_address_id}'.format(
            base_url=self.ip_addresses_url, ip_address_id=ip_address_id)
        resp = self.request('GET', url,
                            response_entity_type=IPAddress,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_ip_addresses(self, ip_address_id=None, network_id=None,
                          address=None, subnet_id=None, port_ids=None,
                          tenant_id=None, version=None,
                          type_=None, port_id=None, device_id=None,
                          service=None, limit=None, marker=None,
                          page_reverse=None, requestslib_kwargs=None):
        """
        @summary: Lists IP addresses, filtered by params if given
        @param ip_address_id: shared IP UUID
        @type ip_address_id: str
        @param network_id: network UUID where the IP address belongs to
        @type network_id: str
        @param address: IP address
        @type address: str
        @param subnet_id: subnet UUID where the IP address belongs to
        @type subnet_id: str
        @param port_ids: IP addresses port UUIDs
        @type port_ids: list
        @param tenant_id: tenant ID of the shared IP user
        @type tenant_id: str
        @param version: IP address version 4 or 6
        @type version: int
        @param type_: IP address type, for ex. fixed
        @type type_: str
        @param port_id: IP address by their port ID
        @type port_id: str (/ip_addresses/{id}/ports child resource attr)
        @param device_id: IP address by their port device ID
        @type device_id: str (/ip_addresses/{id}/ports child resource attr)
        @param service: IP address by their port service, for ex. compute
        @type service: str (/ip_addresses/{id}/ports child resource attr)
        @param limit: page size
        @type limit: int
        @param marker: Id of the last item of the previous page
        @type marker: string
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @return: IP address list response
        @rtype: Requests.response
        """

        params = {'id': ip_address_id, 'network_id': network_id,
                  'address': address, 'subnet_id': subnet_id,
                  'port_ids[]': port_ids, 'tenant_id': tenant_id,
                  'version': version, 'type': type_, 'port_id': port_id,
                  'device_id': device_id, 'service': service,
                  'limit': limit, 'marker': marker,
                  'page_reverse': page_reverse}

        url = self.ip_addresses_url
        resp = self.request('GET', url, params=params,
                            response_entity_type=IPAddresses,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_ip_address(self, ip_address_id, requestslib_kwargs=None):
        """
        @summary: Deletes a specified IP address
        @param ip_address_id: The UUID for the ip_address to delete
        @type ip_address_id: str
        @return: IP address delete response
        @rtype: Requests.response
        """
        url = '{base_url}/{ip_address_id}'.format(
            base_url=self.ip_addresses_url, ip_address_id=ip_address_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
