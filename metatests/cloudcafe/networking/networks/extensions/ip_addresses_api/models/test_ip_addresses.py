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

import unittest

from cloudcafe.networking.networks.extensions.ip_addresses_api.models.request\
    import IPAddressRequest
from cloudcafe.networking.networks.extensions.ip_addresses_api.models.response\
    import IPAddress, IPAddresses


ERROR_MSG_REQ = ('JSON unexpected IP Address request serialization\n'
                 'Actual Serialization:\n{request}\n'
                 'Expected Serialization:\n{expected}\n')
ERROR_MSG_RESP = ('JSON to Obj response different than expected\n'
                  'Actual Response:\n{response}\n'
                  'Expected Response:\n{expected}\n')


class CreateIPAddressTest(unittest.TestCase):
    """
    @summary: Test for the IP Address POST model object request
    """
    @classmethod
    def setUpClass(cls):
        create_attrs = dict(
            network_id='testnet_id', version='4',
            device_ids=['dev1, dev2, dev3'],
            port_ids=['port1', 'port2', 'port3'])
        cls.ip_address_model = IPAddressRequest(**create_attrs)
        cls.expected_json_output = (
            '{"ip_address": {"network_id": "testnet_id", "port_ids": '
            '["port1", "port2", "port3"], "version": "4", "device_ids": '
            '["dev1, dev2, dev3"]}}')

    def test_json_request(self):
        request_body = self.ip_address_model._obj_to_json()
        msg = ERROR_MSG_REQ.format(request=request_body,
                                   expected=self.expected_json_output)
        self.assertEqual(request_body, self.expected_json_output, msg)


class GetIPAddressTest(unittest.TestCase):
    """
    @sumary: Test for the IP Address GET model object response
    """
    @classmethod
    def setUpClass(cls):
        # Setting the expected response object
        get_attrs = dict(
            id_='4cacd68e-d7aa-4ff2-96f4-5c6f57dba737',
            network_id='fda61e0b-a410-49e8-ad3a-64c595618c7e',
            address='192.168.10.1',
            port_ids=['6200d533-a42b-4c04-82a1-cc14dbdbf2de'],
            subnet_id='f11687e8-ef0d-4207-8e22-c60e737e473b',
            tenant_id='2345678',
            version='4',
            type_='fixed')
        cls.expected_response = IPAddress(**get_attrs)

        # Data simulating the JSON API response
        cls.api_json_resp = ("""
            {
                "ip_address": {
                    "id": "4cacd68e-d7aa-4ff2-96f4-5c6f57dba737",
                    "network_id": "fda61e0b-a410-49e8-ad3a-64c595618c7e",
                    "address": "192.168.10.1",
                    "port_ids": ["6200d533-a42b-4c04-82a1-cc14dbdbf2de"],
                    "subnet_id": "f11687e8-ef0d-4207-8e22-c60e737e473b",
                    "tenant_id": "2345678",
                    "version": "4",
                    "type": "fixed"}
            }
        """)

    def test_json_response(self):
        response_obj = IPAddress()._json_to_obj(self.api_json_resp)
        msg = ERROR_MSG_RESP.format(response=response_obj,
                                    expected=self.expected_response)
        self.assertEqual(response_obj, self.expected_response, msg)


class ListIPAddressesTest(unittest.TestCase):
    """
    @sumary: Test for the IP Addresses (List) GET model object response
    """
    @classmethod
    def setUpClass(cls):
        # Setting the expected response object
        get_attrs1 = dict(
            id_='address',
            network_id='fda61e0b-a410-49e8-ad3a-64c595618c7e',
            address='192.168.10.1',
            port_ids=['6200d533-a42b-4c04-82a1-cc14dbdbf2de'],
            subnet_id='f11687e8-ef0d-4207-8e22-c60e737e473b',
            tenant_id='2345678',
            version='4',
            type_='fixed')
        get_attrs2 = dict(
            id_='address2',
            network_id='a_network_id',
            address='192.168.10.7',
            port_ids=['port_id1', 'port_id2', 'port_id3'],
            subnet_id='a_subnet_id',
            tenant_id='a_tenant_id',
            version='6',
            type_='floating')
        ip_address1 = IPAddress(**get_attrs1)
        ip_address2 = IPAddress(**get_attrs2)
        cls.expected_response = [ip_address1, ip_address2]

        # Data simulating the JSON API response
        cls.api_json_resp = ("""
            {
                "ip_addresses": [{
                    "id": "address",
                    "network_id": "fda61e0b-a410-49e8-ad3a-64c595618c7e",
                    "address": "192.168.10.1",
                    "port_ids": ["6200d533-a42b-4c04-82a1-cc14dbdbf2de"],
                    "subnet_id": "f11687e8-ef0d-4207-8e22-c60e737e473b",
                    "tenant_id": "2345678",
                    "version": "4",
                    "type": "fixed"},
                    {
                    "id": "address2",
                    "network_id": "a_network_id",
                    "address": "192.168.10.7",
                    "port_ids": ["port_id1", "port_id2", "port_id3"],
                    "subnet_id": "a_subnet_id",
                    "tenant_id": "a_tenant_id",
                    "version": "6",
                    "type": "floating"}]
            }
        """)

    def test_json_response(self):
        response_obj = IPAddresses()._json_to_obj(self.api_json_resp)
        msg = ERROR_MSG_RESP.format(response=response_obj,
                                    expected=self.expected_response)
        self.assertEqual(response_obj, self.expected_response, msg)


if __name__ == "__main__":
    unittest.main()
