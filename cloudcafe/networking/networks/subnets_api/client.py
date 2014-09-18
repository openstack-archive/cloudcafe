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
from cloudcafe.networking.networks.common.models.request.subnet \
    import SubnetRequest
from cloudcafe.networking.networks.common.models.response.subnet \
    import Subnet, Subnets


class SubnetsClient(AutoMarshallingHTTPClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None, tenant_id=None):
        """
        @param url: Base URL for the subnets service
        @type url: string
        @param auth_token: Auth token to be used for all requests
        @type auth_token: string
        @param serialize_format: Format for serializing requests
        @type serialize_format: string
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: string
        @param tenant_id: optional tenant id to be included in the header if
            given
        @type tenant_id: string
        """
        super(SubnetsClient, self).__init__(serialize_format,
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

    def create_subnet(self, network_id, ip_version, cidr, name=None,
                      tenant_id=None, gateway_ip=None, dns_nameservers=None,
                      allocation_pools=None, host_routes=None,
                      enable_dhcp=None, requestslib_kwargs=None):
        """
        @summary: Creates a Subnet
        @param name: human readable name for the subnet, may not be unique
            (CRUD: CRU)
        @type name: string
        @param tenant_id: owner of the network. (CRUD: CR)
        @type tenant_id: string
        @param network_id: network subnet is associated with (CRUD: CR)
        @type network_id: string
        @param ip_version: IP version 4 or 6 (CRUD: CR)
        @type ip_version: int
        @param cidr: represents IP range for the subnet and should be in the
            form <network_address>/<prefix> (CRUD: CR)
        @type cidr: string
        @param gateway_ip: default gateway used by devices in the subnet
            (CRUD: CRUD)
        @type gateway_ip: string
        @param dns_nameservers: DNS name servers used by subnet hosts
            (CRUD: CRU)
        @type dns_nameservers: list(str)
        @param allocation_pools: sub range of cidr available for dynamic
            allocation to ports (CRUD: CRU)
        @type allocation_pools: list(dict)
        @param host_routes: routes that should be used by devices with IPs
            from this subnet (does not includes the local route, CRUD: CRU)
        @type host_routes: list(dict)
        @param enable_dhcp: whether DHCP is enabled (CRUD:CRU)
        @type enable_dhcp: bool
        @return: subnet create response
        @rtype: Requests.response
        """
        url = '{base_url}/subnets'.format(base_url=self.url)

        request = SubnetRequest(network_id=network_id, ip_version=ip_version,
                                cidr=cidr, name=name, tenant_id=tenant_id,
                                gateway_ip=gateway_ip,
                                dns_nameservers=dns_nameservers,
                                allocation_pools=allocation_pools,
                                host_routes=host_routes,
                                enable_dhcp=enable_dhcp)

        resp = self.request('POST', url,
                            response_entity_type=Subnet,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def update_subnet(self, subnet_id, name=None, gateway_ip=None,
                      dns_nameservers=None, host_routes=None,
                      enable_dhcp=None, allocation_pools=None,
                      requestslib_kwargs=None):
        """
        @summary: Updates a specified Subnet
        @param subnet_id: The UUID for the subnet
        @type subnet_id: string
        @param name: human readable name for the subnet, may not be unique
            (CRUD: CRU)
        @type name: string
        @param gateway_ip: default gateway used by devices in the subnet
            (CRUD: CRUD)
        @type gateway_ip: string
        @param dns_nameservers: DNS name servers used by subnet hosts
            (CRUD: CRU)
        @type dns_nameservers: list(str)
        @param host_routes: routes that should be used by devices with IPs
            from this subnet (does not includes the local route (CRUD: CRU)
        @type host_routes: list(dict)
        @param enable_dhcp: whether DHCP is enabled (CRUD:CRU)
        @type enable_dhcp: bool
        @param allocation_pools: sub range of cidr available for dynamic
            allocation to ports (CRUD: CRU)
        @type allocation_pools: list(dict)
        @return: subnet update response
        @rtype: Requests.response
        """

        url = '{base_url}/subnets/{subnet_id}'.format(
            base_url=self.url, subnet_id=subnet_id)

        request = SubnetRequest(name=name, gateway_ip=gateway_ip,
                                dns_nameservers=dns_nameservers,
                                host_routes=host_routes,
                                enable_dhcp=enable_dhcp,
                                allocation_pools=allocation_pools)
        resp = self.request('PUT', url,
                            response_entity_type=Subnet,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_subnet(self, subnet_id, requestslib_kwargs=None):
        """
        @summary: Shows information for a specified subnet
        @param subnet_id: The UUID for the subnet
        @type subnet_id: string
        @return: get subnet response
        @rtype: Requests.response
        """

        url = '{base_url}/subnets/{subnet_id}'.format(
            base_url=self.url, subnet_id=subnet_id)
        resp = self.request('GET', url,
                            response_entity_type=Subnet,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_subnets(self, subnet_id=None, network_id=None, cidr=None,
                     tenant_id=None, gateway_ip=None, ip_version=None,
                     enable_dhcp=None, name=None, limit=None, marker=None,
                     page_reverse=None, requestslib_kwargs=None):
        """
        @summary: Lists subnets, filtered by params if given
        @param subnet_id: subnet ID to filter by
        @type subnet_id: string
        @param network_id: network ID to filter by
        @type network_id: string
        @param cidr: cider to filter by
        @type cidr: string
        @param tenant_id: owner of the network to filter by
        @type tenant_id: string
        @param gateway_ip: gateway_ip to filter by
        @type gateway_ip: string
        @param ip_version: IP version 4 or 6 to filter by
        @type ip_version: int
        @param enable_dhcp: enable_dhcp status to filter by
        @type enable_dhcp: bool
        @param name: subnet name to filter by
        @type name: string
        @param limit: page size
        @type limit: int
        @param marker: Id of the last item of the previous page
        @type marker: string
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @return: list subnet response
        @rtype: Requests.response
        """

        params = {'id': subnet_id, 'network_id': network_id, 'cidr': cidr,
                  'tenant_id': tenant_id, 'gteway_ip': gateway_ip,
                  'ip_version': ip_version, 'enable_dhcp': enable_dhcp,
                  'name': name, 'limit': limit, 'marker': marker,
                  'page_reverse': page_reverse}
        url = '{base_url}/subnets'.format(base_url=self.url)
        resp = self.request('GET', url, params=params,
                            response_entity_type=Subnets,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_subnet(self, subnet_id, requestslib_kwargs=None):
        """
        @summary: Deletes a specified subnet
        @param subnet_id: The UUID for the subnet
        @type subnet_id: string
        @return: delete subnet response
        @rtype: Requests.response
        """

        url = '{base_url}/subnets/{subnet_id}'.format(
            base_url=self.url, subnet_id=subnet_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
