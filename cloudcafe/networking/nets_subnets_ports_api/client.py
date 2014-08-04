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

from cloudcafe.common.client import BaseClient, setup_rest_operation


class NetsSubnetsPortsClient(BaseClient):
    """Implements the Neutron ReST client for the following API resources:

        networks
        subnets
        ports
    """

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        """
        @param url: Base URL for the Neutron service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """
        super(NetsSubnetsPortsClient, self).__init__(url, auth_token,
                                                     serialize_format,
                                                     deserialize_format)
        self._models_classes = {'networks': (None, None),
                                'subnets': (None, None),
                                'ports': (None, None), }
        self._resource_plural_map = {}

    @setup_rest_operation
    def list_networks(self, name=None, admin_state_up=None, status=None,
                      shared=None, tenant_id=None, limit=None, marker=None,
                      page_reverse=None, requestslib_kwargs=None):
        """
        @summary: Lists all networks. Additionally, can filter results by
         params. Maps to /networks
        @param name: Network name to filter by
        @type name: String
        @param admin_state_up: Network administrative state up value to filter
         by
        @type admin_state_up: Boolean
        @param status: Network status to filter by
        @type status: String
        @param shared: Network shared attribute value to filter by
        @type shared: Boolean
        @param tenant_id: Network owner tenant_id to filter by
        @type tenant_id: String
        @param marker: Network id to be used as a marker for the next list
        @type marker: String
        @param limit: The maximum number of results to return
        @type limit: Int
        @param page_reverse: Page direction setting
        @type page_reverse: Boolean
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._list(name=name, admin_state_up=admin_state_up,
                          status=status, shared=shared, tenant_id=tenant_id,
                          marker=marker, limit=limit,
                          page_reverse=page_reverse,
                          requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def create_network(self, name, admin_state_up=None, shared=None,
                       tenant_id=None, requestslib_kwargs=None):
        """
        @summary: Creates an instance of a network given the
         provided parameters
        @param name: human readable name of the network. Might not be unique.
         No default value provided by the API
        @type name: String
        @param admin_state_up: Network administrative state up value. If down,
         the network does not forward packets. API default value is true
        @type admin_state_up: Boolean
        @param shared: Specifies whether the network can be shared by other
         tenants or not. API default value is false
        @type shared: Boolean
        @param tenant_id: owner of network. Only admin users can specify a
         tenant id other than its own. No default value provided by the API
        @type tenant_id: String
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._create(name=name, admin_state_up=admin_state_up,
                            shared=shared, tenant_id=tenant_id,
                            requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def update_network(self, network_id, name=None, admin_state_up=None,
                       shared=None, requestslib_kwargs=None):
        """
        @summary: updates an instance of a network given the
         provided parameters
        @param network_id: id of the network to update
        @type network_id: String
        @param name: human readable name of the network. Might not be unique.
        @type name: String
        @param admin_state_up: Network administrative state up value. If down,
         the network does not forward packets.
        @type admin_state_up: Boolean
        @param shared: Specifies whether the network can be shared by other
         tenants or not.
        @type shared: Boolean
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._update(network_id, name=name,
                            admin_state_up=admin_state_up, shared=shared,
                            requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def show_network(self, network_id, requestslib_kwargs=None):
        """
        @summary: get the attributes of a network instance
        @param network_id: id of the network whose attributes will be gotten
        @type network_id: String
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._show(network_id, requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def delete_network(self, network_id, requestslib_kwargs=None):
        """
        @summary: delete a network
        @param network_id: id of the network to delete
        @type network_id: String
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._delete(network_id, requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def list_subnets(self, network_id=None, name=None, ip_version=None,
                     cidr=None, gateway_ip=None, enable_dhcp=None,
                     tenant_id=None, limit=None, marker=None,
                     page_reverse=None, requestslib_kwargs=None):
        """
        @summary: Lists all subnets. Additionally, can filter results by
         params. Maps to /subnets
        @param network_id: Network id to filter by
        @type network_id: String
        @param name: Subnet id to filter by
        @type name: String
        @param ip_version: IP version to filter by
        @type ip_version: Int
        @param cidr: cidr to filter by
        @type cidr: String
        @param gateway_ip: Gateway ip address to filter by
        @type gateway_ip: String
        @param enable_dhcp: Enable dhcp setting to filter by
        @type enable_dhcp: Boolen
        @param tenant_id: ID of tenant to filter by
        @type tenant_id: String
        @param marker: Subnet id to be used as a marker for the next list
        @type marker: String
        @param limit: The maximum number of results to return
        @type limit: Int
        @param page_reverse: Page direction setting
        @type page_reverse: Boolean
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._list(network_id=network_id, name=name,
                          ip_version=ip_version, cidr=cidr,
                          gateway_ip=gateway_ip, enable_dhcp=enable_dhcp,
                          tenant_id=tenant_id,  marker=marker, limit=limit,
                          page_reverse=page_reverse,
                          requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def create_subnet(self, network_id, cidr, name=None, ip_version=None,
                      gateway_ip=None, dns_nameservers=None,
                      allocation_pools=None, host_routes=None,
                      enable_dhcp=None, tenant_id=None,
                      requestslib_kwargs=None):
        """
        @summary: Creates an instance of a subnet given the
         provided parameters
        @param network_id: the id of the network the subnet will be
         associated with
        @type network_id: String
        @param cidr: the ip range for the subnet
        @type cidr: String
        @param name: human readable name for the subnet. Might not be unique.
         No default value provided by the API
        @type name: String
        @param ip_version: the IP version for the subnet. API default value is
         4
        @type ip_version: Int
        @param gateway_ip: default gateway used by devices in the subnet
         API default value is the first address in the cidr
        @type gateway_ip: String
        @param dns_nameservers: DNS nanme servers used by hosts in the subnet
         API default value is an empty list
        @type dns_nameservers: List of String
        @param allocation_pools: sub-ranges of cidr available for dynamic
         allocation to ports. API default value is every address in cidr,
         excluding gateway ip if configured
        @type allocation_pools: List of Dictionaries
        @param host_routes: routes that should be used by devices with IP's
         from the subnet (not including local subnet route). API default value
         is empty list
        @type host_routes: List of Dictionaries
        @param enable_dhcp: specifies whether DHCP is enabled for the subnet or
         not. API default value is true
        @type enable_dhcp: Boolean
        @param tenant_id: owner of subnet. Only admin users can specify a
         tenant id other than its own. No default value provided by the API
        @type tenant_id: String
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._create(network_id=network_id, cidr=cidr, name=name,
                            ip_version=ip_version, gateway_ip=gateway_ip,
                            dns_nameservers=dns_nameservers,
                            allocation_pools=allocation_pools,
                            host_routes=host_routes, enable_dhcp=enable_dhcp,
                            tenant_id=tenant_id,
                            requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def update_subnet(self, subnet_id, name=None, gateway_ip=None,
                      dns_nameservers=None, host_routes=None,
                      enable_dhcp=None, requestslib_kwargs=None):
        """
        @summary: updates an instance of a subnet given the
         provided parameters
        @param subnet_id: the id of the subnet to updtes
        @type subnet_id: String
        @param name: human readable name for the subnet. Might not be unique.
        @type name: String
        @param gateway_ip: default gateway used by devices in the subnet
        @type gateway_ip: String
        @param dns_nameservers: DNS nanme servers used by hosts in the subnet
        @type dns_nameservers: List of String
        @param host_routes: routes that should be used by devices with IP's
         from the subnet (not including local subnet route).
        @type host_routes: List of Dictionaries
        @param enable_dhcp: specifies whether DHCP is enabled for the subnet or
         not.
        @type enable_dhcp: Boolean
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._update(subnet_id, name=name, gateway_ip=gateway_ip,
                            dns_nameservers=dns_nameservers,
                            host_routes=host_routes, enable_dhcp=enable_dhcp,
                            requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def show_subnet(self, subnet_id, requestslib_kwargs=None):
        """
        @summary: get the attributes of a subnet instance
        @param subnet_id: id of the subnet whose attributes will be gotten
        @type subnet_id: String
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._show(subnet_id, requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def delete_subnet(self, subnet_id, requestslib_kwargs=None):
        """
        @summary: delete a subnet
        @param subnet_id: id of the subnet to delete
        @type subnet_id: String
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._delete(subnet_id, requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def list_ports(self, network_id=None, name=None, admin_state_up=None,
                   status=None, mac_address=None, device_id=None,
                   device_owner=None, tenant_id=None, limit=None, marker=None,
                   page_reverse=None, requestslib_kwargs=None):
        """
        @summary: Lists all ports. Additionally, can filter results by
         params. Maps to /ports
        @param network_id: Network id to filter by
        @type network_id: String
        @param name: Port id to filter by
        @type name: String
        @param admin_state_up: Network administrative state up value to filter
         by
        @type admin_state_up: Boolean
        @param status: Network status to filter by
        @type status: String
        @param mac_address: mac_address to filter by
        @type mac_address: String
        @param device_id: Device id to filter by
        @type device_id: String
        @param device_owner: Device owner to filter by
        @type device_owner: String
        @param tenant_id: ID of tenant to filter by
        @type tenant_id: String
        @param marker: Subnet id to be used as a marker for the next list
        @type marker: String
        @param limit: The maximum number of results to return
        @type limit: Int
        @param page_reverse: Page direction setting
        @type page_reverse: Boolean
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._list(network_id=network_id, name=name,
                          admin_state_up=admin_state_up, status=status,
                          mac_address=mac_address, device_id=device_id,
                          device_owner=device_owner, tenant_id=tenant_id,
                          marker=marker, limit=limit,
                          page_reverse=page_reverse,
                          requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def create_port(self, network_id, name=None, admin_state_up=None,
                    mac_address=None, fixed_ips=None, device_id=None,
                    device_owner=None, tenant_id=None, security_groups=None,
                    requestslib_kwargs=None):
        """
        @summary: Creates an instance of a port given the
         provided parameters
        @param network_id: network that the port is associated with. No default
         value provided by the API
        @type neywork_id: String
        @param name: hurman readable name for the port. Might not be unique. No
         default value provided by the API
        @type name: String
        @param admin_state_up: administrative state of the port. If false, port
         does not forward packets. API default value is true
        @type admin_state_up: Boolean
        @param mac_address: mac addres to be used on this port. API default
         value is generated
        @type mac_address: String
        @param fixed_ips: specifies ip adddreses for the port, associating it
         with the subnets where the ip addresses are picked from. API default
         value is an ip address selected from the allocation pools associated
         with the network
        @type fixed_ips: List of Dictionaries
        @param device_id: identifies the device (e.g. virtual server) using the
         port. No default value provided by the API
        @type device_id: String
        @param device_owner: identifies the entity (e.g. dhcp agent) using the
         port. No default value provided by the API
        @type device_owner: String
        @param tenant_id: owner of port. Only admin users can specify tenants
         other than their own. No default value provided by the API
        @type tenant_id: String
        @param security_groups: specifies the ID's of any security groups
         associated with the port. No default value provided by the API
        @type security_groups: List of Dictionaries
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._create(network_id=network_id, name=name,
                            admin_state_up=admin_state_up,
                            mac_address=mac_address, fixed_ips=fixed_ips,
                            device_id=device_id, device_owner=device_owner,
                            tenant_id=tenant_id,
                            security_groups=security_groups,
                            requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def update_port(self, port_id, name=None, admin_state_up=None,
                    fixed_ips=None, device_id=None, device_owner=None,
                    security_groups=None, requestslib_kwargs=None):
        """
        @summary: updates an instance of a port given the
         provided parameters
        @param port_id: id of the port to be updated
        @type neywork_id: String
        @param name: hurman readable name for the port. Might not be unique.
        @type name: String
        @param admin_state_up: administrative state of the port. If false, port
         does not forward packets.
        @type admin_state_up: Boolean
        @param fixed_ips: specifies ip adddreses for the port, associating it
         with the subnets where the ip addresses are picked from.
        @type fixed_ips: List of Dictionaries
        @param device_id: identifies the device (e.g. virtual server) using the
         port.
        @type device_id: String
        @param device_owner: identifies the entity (e.g. dhcp agent) using the
         port.
        @type device_owner: String
        @param security_groups: specifies the ID's of any security groups
         associated with the port
        @type security_groups: List of Dictionaries
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._update(port_id, name=name, admin_state_up=None,
                            fixed_ips=fixed_ips, device_id=device_id,
                            device_owner=device_owner,
                            security_groups=security_groups,
                            requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def show_port(self, port_id, requestslib_kwargs=None):
        """
        @summary: get the attributes of a port instance
        @param port_id: id of the port whose attributes will be gotten
        @type port_id: String
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._show(port_id, requestslib_kwargs=requestslib_kwargs)

    @setup_rest_operation
    def delete_port(self, port_id, requestslib_kwargs=None):
        """
        @summary: delete a port
        @param port_id: id of the port to be deleted
        @type port_id: String
        @param requestslib_kwargs: keyword arguments to be passed to the
         requests library
        @type requestslib_kwargs: Dictionary
        @return: response from the API
        @rtype: Requests.response
        """
        return self._delete(port_id, requestslib_kwargs=requestslib_kwargs)
