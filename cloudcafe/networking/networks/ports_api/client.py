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
        @param string url: Base URL for the ports service
        @param string auth_token: Auth token to be used for all requests
        @param string serialize_format: Format for serializing requests
        @param string deserialize_format: Format for de-serializing responses
        @param string tenant_id: optional tenant id to be included in the
            header if given
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
        @param string network_id: network port is associated with (CRUD: CR)
        @param string name: human readable name for the port,
            may not be unique. (CRUD: CRU)
        @param bool admin_state_up: true or false (default true),
            the admin state of the port. If down, the port does not forward
            packets (CRUD: CRU)
        @param string mac_address: mac address to use on the port (CRUD: CR)
        @param list(dict) fixed_ips: ip addresses for the port associating the
            port with the subnets where the IPs come from (CRUD: CRU)
        @param string device_id: id of device using this port (CRUD: CRUD)
        @param string device_owner: entity using this port (ex. dhcp agent,
            CRUD: CRUD)
        @param string tenant_id: owner of the port (CRUD: CR)
        @param list(dict) security_groups: ids of any security groups
            associated with the port (CRUD: CRUD)
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
        @param string port_id: The UUID for the port
        @param string name: human readable name for the port,
            may not be unique. (CRUD: CRU)
        @param bool admin_state_up: true or false (default true),
            the admin state of the port. If down, the port does not forward
            packets (CRUD: CRU)
        @param list(dict) fixed_ips: ip addresses for the port associating the
            port with the subnets where the IPs come from (CRUD: CRU)
        @param string device_id: id of device using this port (CRUD: CRUD)
        @param string device_owner: entity using this port (ex. dhcp agent,
            CRUD: CRUD)
        @param list(dict) security_groups: ids of any security groups
            associated with the port (CRUD: CRUD)
        """

        url = '{base_url}/ports/{port_id}'.format(
            base_url=self.url, port_id=port_id)

        request = PortRequest(name=name, admin_state_up=admin_state_up,
            fixed_ips=fixed_ips, device_id=device_id,
            device_owner=device_owner, security_groups=security_groups)
        resp = self.request('PUT', url,
                            response_entity_type=Port,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_port(self, port_id, requestslib_kwargs=None):
        """
        @summary: Shows information for a specified port
        @param string port_id: The UUID for the port
        """

        url = '{base_url}/ports/{port_id}'.format(
            base_url=self.url, port_id=port_id)
        resp = self.request('GET', url,
                            response_entity_type=Port,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_ports(self, requestslib_kwargs=None):
        """
        @summary: Lists ports
        """

        # TODO: add field query params to filter the response
        url = '{base_url}/ports'.format(base_url=self.url)
        resp = self.request('GET', url,
                            response_entity_type=Ports,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_port(self, port_id, requestslib_kwargs=None):
        """
        @summary: Deletes a specified port
        @param string port_id: The UUID for the port
        """

        url = '{base_url}/ports/{port_id}'.format(
            base_url=self.url, port_id=port_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
