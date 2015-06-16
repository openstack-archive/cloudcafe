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
from cloudcafe.networking.networks.common.models.request.port \
    import PortRequest
from cloudcafe.networking.networks.common.models.response.port \
    import Port, Ports


class PortsClient(AutoMarshallingHTTPClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None, tenant_id=None):
        """
        @param url: Base URL for the ports service
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
        super(PortsClient, self).__init__(serialize_format,
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

    def create_port(self, network_id, name=None, admin_state_up=None,
                    mac_address=None, fixed_ips=None, device_id=None,
                    device_owner=None, tenant_id=None, security_groups=None,
                    requestslib_kwargs=None):
        """
        @summary: Creates a Port
        @param network_id: network port is associated with (CRUD: CR)
        @type network_id: string
        @param name: human readable name for the port,
            may not be unique. (CRUD: CRU)
        @type name: string
        @param admin_state_up: true or false (default true),
            the admin state of the port. If down, the port does not forward
            packets (CRUD: CRU)
        @type admin_state_up: bool
        @param mac_address: mac address to use on the port (CRUD: CR)
        @type mac_address: string
        @param fixed_ips: ip addresses for the port associating the port with
            the subnets where the IPs come from (CRUD: CRU)
        @type fixed_ips: list(dict)
        @param device_id: id of device using this port (CRUD: CRUD)
        @type device_id: string
        @param device_owner: entity using this port (ex. dhcp agent,CRUD: CRUD)
        @type device_owner: string
        @param tenant_id: owner of the port (CRUD: CR)
        @type tenant_id: string
        @param security_groups: ids of any security groups associated with the
            port (CRUD: CRUD)
        @type security_groups: list(dict)
        @return: port create response
        @rtype: Requests.response
        """

        url = '{base_url}/ports'.format(base_url=self.url)

        request = PortRequest(
            network_id=network_id, name=name, admin_state_up=admin_state_up,
            mac_address=mac_address, fixed_ips=fixed_ips, device_id=device_id,
            device_owner=device_owner, tenant_id=tenant_id,
            security_groups=security_groups)

        resp = self.request('POST', url,
                            response_entity_type=Port,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def update_port(self, port_id, name=None, admin_state_up=None,
                    fixed_ips=None, device_id=None, device_owner=None,
                    security_groups=None, requestslib_kwargs=None):
        """
        @summary: Updates a specified Port
        @param port_id: The UUID for the port
        @type port_id: string
        @param name: human readable name for the port, may not be unique
            (CRUD: CRU)
        @type name: string
        @param admin_state_up: true or false (default true), the admin state
            of the port. If down, the port does not forward packets (CRUD: CRU)
        @type admin_state_up: bool
        @param fixed_ips: ip addresses for the port associating the port with
            the subnets where the IPs come from (CRUD: CRU)
        @type fixed_ips: list(dict)
        @param device_id: id of device using this port (CRUD: CRUD)
        @type device_id: string
        @param string device_owner: entity using this port (ex. dhcp agent,
            CRUD: CRUD)
        @type device_owner: string
        @param security_groups: ids of any security groups associated with the
            port (CRUD: CRUD)
        @type security_groups: list(dict)
        @return: update port response
        @rtype: Requests.response
        """

        url = '{base_url}/ports/{port_id}'.format(
            base_url=self.url, port_id=port_id)

        request = PortRequest(
            name=name, admin_state_up=admin_state_up, fixed_ips=fixed_ips,
            device_id=device_id, device_owner=device_owner,
            security_groups=security_groups)
        resp = self.request('PUT', url,
                            response_entity_type=Port,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_port(self, port_id, requestslib_kwargs=None):
        """
        @summary: Shows information for a specified port
        @param port_id: The UUID for the port
        @type port_id: string
        @return: get port response
        @rtype: Requests.response
        """

        url = '{base_url}/ports/{port_id}'.format(
            base_url=self.url, port_id=port_id)
        resp = self.request('GET', url,
                            response_entity_type=Port,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_ports(self, port_id=None, network_id=None, name=None, status=None,
                   admin_state_up=None, device_id=None, tenant_id=None,
                   device_owner=None, mac_address=None, limit=None,
                   marker=None, page_reverse=None, requestslib_kwargs=None):
        """
        @summary: Lists ports, filtered by params if given
        @param port_id: The UUID for the port to filter by
        @type port_id: string
        @param network_id: network ID to filter by
        @type network_id: string
        @param name: port name to filter by
        @type name: string
        @param status: port status to filter by
        @type status: string
        @param admin_state_up: Admin state of the port to filter by
        @type admin_state_up: bool
        @param device_id: id of device to filter by
        @type device_id: string
        @param tenant_id: owner of the port to filter by
        @type tenant_id: string
        @param device_owner: device owner to filter by
        @type device_owner: string
        @param mac_address: mac address to filter by
        @type mac_address: string
        @param limit: page size
        @type limit: int
        @param marker: Id of the last item of the previous page
        @type marker: string
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @return: list ports response
        @rtype: Requests.response
        """

        params = {'id': port_id, 'network_id': network_id, 'name': name,
                  'status': status, 'admin_state_up': admin_state_up,
                  'device_id': device_id, 'tenant_id': tenant_id,
                  'device_owner': device_owner, 'mac_address': mac_address,
                  'limit': limit, 'marker': marker,
                  'page_reverse': page_reverse}
        url = '{base_url}/ports'.format(base_url=self.url)
        resp = self.request('GET', url, params=params,
                            response_entity_type=Ports,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_port(self, port_id, requestslib_kwargs=None):
        """
        @summary: Deletes a specified port
        @param string port_id: The UUID for the port
        @type port_id: string
        @return: delete port response
        @rtype: Requests.response
        """

        url = '{base_url}/ports/{port_id}'.format(
            base_url=self.url, port_id=port_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
