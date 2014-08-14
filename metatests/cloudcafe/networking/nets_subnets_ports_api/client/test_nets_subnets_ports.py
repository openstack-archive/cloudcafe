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

from cloudcafe.networking.nets_subnets_ports_api.client\
    import NetsSubnetsPortsClient
from metatests.cloudcafe.networking.common.client.base\
    import BaseNetworkingTest
from metatests.cloudcafe.networking.nets_subnets_ports_api.client.responses\
    import NetworksMockResponse, ListNetworksMockResponse,\
    SubnetsMockResponse, ListSubnetsMockResponse, PortsMockResponse,\
    ListPortsMockResponse


class NetsSubnetsPortsTest(BaseNetworkingTest):

    @classmethod
    def setUpClass(cls):
        super(NetsSubnetsPortsTest, cls).setUpClass()
        cls.client = NetsSubnetsPortsClient(
            url=cls.NETWORKING_API_ENDPOINT,
            auth_token=cls.AUTH_TOKEN,
            serialize_format=cls.FORMAT,
            deserialize_format=cls.FORMAT)

    def test_create_network(self):
        expected_request_body = (
            '{"network":'
            '{"name": "nuevo_miguelito",'
            '"admin_state_up": false}}')
        self._test_create('network', NetworksMockResponse,
                          expected_request_body,
                          name='nuevo_miguelito',
                          admin_state_up=False)

    def test_update_network(self):
        expected_request_body = (
            '{"network":'
            '{"name": "nuevo_miguelito",'
            '"admin_state_up": false}}')
        self._test_update('network', '97a5cb31-bdc4-48c0-b04f-34ab551053e1',
                          NetworksMockResponse, expected_request_body,
                          network_id='97a5cb31-bdc4-48c0-b04f-34ab551053e1',
                          name='nuevo_miguelito', admin_state_up=False)
        return

    def test_show_network(self):
        self._test_show('network', '97a5cb31-bdc4-48c0-b04f-34ab551053e1',
                        NetworksMockResponse,
                        network_id='97a5cb31-bdc4-48c0-b04f-34ab551053e1')

    def test_delete_network(self):
        self._test_delete('network', '97a5cb31-bdc4-48c0-b04f-34ab551053e1',
                          network_id='97a5cb31-bdc4-48c0-b04f-34ab551053e1')

    def test_list_networks(self):
        self._test_list('network', ListNetworksMockResponse)

    def test_create_subnet(self):
        expected_request_body = (
            '{"subnet": '
            '{"name": "nuevo_miguelito",'
            '"network_id": "97a5cb31-bdc4-48c0-b04f-34ab551053e1",'
            '"ip_version": 4,'
            '"cidr": "10.0.1.0/24",'
            '"enable_dhcp": true}}')
        self._test_create('subnet', SubnetsMockResponse,
                          expected_request_body,
                          network_id="97a5cb31-bdc4-48c0-b04f-34ab551053e1",
                          cidr="10.0.1.0/24", name="miguelito", ip_version=4,
                          enable_dhcp=True)

    def test_update_subnet(self):
        expected_request_body = (
            '{"subnet":'
            '{"name": "nuevo_miguelito",'
            '"host_routes": ['
            '{"destination": "100.0.0.0/24",'
            '"nexthop": "10.0.1.1"}]}}')
        self._test_update('subnet', 'efee1b83-0084-4a45-b676-38b554188f22',
                          SubnetsMockResponse,
                          expected_request_body,
                          subnet_id='efee1b83-0084-4a45-b676-38b554188f22',
                          name='nuevo_miguelito',
                          host_routes=[{"destination": "100.0.0.0/24",
                                        "nexthop": "10.0.1.1"}])

    def test_show_subnet(self):
        self._test_show('subnet', 'efee1b83-0084-4a45-b676-38b554188f22',
                        SubnetsMockResponse,
                        subnet_id='efee1b83-0084-4a45-b676-38b554188f22')

    def test_list_subnets(self):
        self._test_list('subnet', ListSubnetsMockResponse)

    def test_delete_subnet(self):
        self._test_delete('subnet', 'efee1b83-0084-4a45-b676-38b554188f22',
                          subnet_id='efee1b83-0084-4a45-b676-38b554188f22')

    def test_create_port(self):
        expected_request_body = (
            '{"port":'
            '{"network_id": "97a5cb31-bdc4-48c0-b04f-34ab551053e1",'
            '"name": "nuevo_miguelito",'
            '"admin_state_up": false}}')
        self._test_create('port', PortsMockResponse,
                          expected_request_body,
                          network_id="97a5cb31-bdc4-48c0-b04f-34ab551053e1",
                          name="nuevo_miguelito", admin_state_up=False)

    def test_update_port(self):
        expected_request_body = (
            '{"port":'
            '{"name": "nuevo_miguelito",'
            '"admin_state_up": false,'
            '"fixed_ips": ['
            '{"subnet_id": "efee1b83-0084-4a45-b676-38b554188f22",'
            '"ip_address": "10.0.1.25"}]}}')
        self._test_update(
            'port', "25a658c7-4773-46ce-9bf3-52fc87176b07",
            PortsMockResponse,
            expected_request_body,
            port_id="25a658c7-4773-46ce-9bf3-52fc87176b07",
            name="nuevo_miguelito", admin_state_up=False,
            fixed_ips=[
                {"subnet_id": "efee1b83-0084-4a45-b676-38b554188f22",
                 "ip_address": "10.0.1.25"}])

    def test_show_port(self):
        self._test_show('port', "25a658c7-4773-46ce-9bf3-52fc87176b07",
                        PortsMockResponse,
                        port_id="25a658c7-4773-46ce-9bf3-52fc87176b07")

    def test_list_ports(self):
        self._test_list('port', ListPortsMockResponse)

    def test_delete_port(self):
        self._test_delete('port', "25a658c7-4773-46ce-9bf3-52fc87176b07",
                          port_id="25a658c7-4773-46ce-9bf3-52fc87176b07")
