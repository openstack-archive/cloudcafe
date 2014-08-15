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

import unittest2 as unittest

from cloudcafe.networking.networks.common.models.request.subnet \
    import SubnetRequest
from cloudcafe.networking.networks.common.models.response.subnet \
    import Subnet, Subnets


class CreateSubnetTest(unittest.TestCase):
    """Test for the Subnet Create (POST) Model object requests"""
    @classmethod
    def setUpClass(cls):
        create_attrs = dict(
            network_id='d32019d3-bc6e-4319-9c1d-6722fc136a22',
            ip_version=4, cidr='192.168.199.0/24')
        cls.subnet_model = SubnetRequest(**create_attrs)

        # With all possible create attributes
        create_attrs_all = dict(
            name='test_subnet_name', tenant_id='test_tenant_id',
            network_id='test_network_id', ip_version=6, cidr='test_cidr',
            gateway_ip='test_gateway_ip', dns_nameservers=['test_dnsname1',
            'test_dnsname2', 'test_dnsname3'], allocation_pools=[{'start':
            'start_ip', 'end': 'end_ip'}, {'start2': 'start_ip2', 'end2':
            'end_ip2'}, {'start3': 'start_ip3', 'end3': 'end_ip3'}],
            host_routes=[{'route1_key': 'route1_value', 'route1_key2':
            'route1_value2'}, {'route2_key': 'route2_value', 'route2_key2':
            'route2_value2'}], enable_dhcp=True)
        cls.subnet_model_all = SubnetRequest(**create_attrs_all)

    def test_json_request(self):
        """JSON test with create attrs"""
        expected_json_output = (
            '{"subnet": {"network_id": "d32019d3-bc6e-4319-9c1d-6722fc136a22",'
            ' "ip_version": 4, "cidr": "192.168.199.0/24"}}')
        request_body = self.subnet_model._obj_to_json()
        msg = ('Unexpected JSON Subnet request serialization. Expected {0} '
               'instead of {1}'.format(expected_json_output, request_body))
        self.assertEqual(request_body, expected_json_output, msg)

    def test_json_request_all_attrs(self):
        """JSON test with all create attrs"""
        expected_json_output = (
            '{"subnet": {"name": "test_subnet_name", "enable_dhcp": true, '
            '"network_id": "test_network_id", "tenant_id": "test_tenant_id", '
            '"dns_nameservers": ["test_dnsname1", "test_dnsname2", '
            '"test_dnsname3"], "allocation_pools": [{"start": "start_ip", '
            '"end": "end_ip"}, {"start2": "start_ip2", "end2": "end_ip2"}, '
            '{"start3": "start_ip3", "end3": "end_ip3"}], "gateway_ip": '
            '"test_gateway_ip", "ip_version": 6, "host_routes": '
            '[{"route1_key2": "route1_value2", "route1_key": "route1_value"}, '
            '{"route2_key2": "route2_value2", "route2_key": "route2_value"}], '
            '"cidr": "test_cidr"}}')
        request_body = self.subnet_model_all._obj_to_json()
        msg = ('Unexpected JSON Subnet request serialization. Expected {0} '
               'instead of {1}'.format(expected_json_output, request_body))
        self.assertEqual(request_body, expected_json_output, msg)


class UpdateSubnetTest(unittest.TestCase):
    """Test for the Subnet Update (PUT) Model object requests"""
    @classmethod
    def setUpClass(cls):
        update_attrs = dict(
            name='test_subnet_name', gateway_ip='test_gateway_ip',
            dns_nameservers=['test_dnsname1', 'test_dnsname2',
            'test_dnsname3'], host_routes=[{'route1_key': 'route1_value',
            'route1_key2': 'route1_value2'}, {'route2_key': 'route2_value',
            'route2_key2': 'route2_value2'}], enable_dhcp=True)
        cls.subnet_model = SubnetRequest(**update_attrs)

    def test_json_request(self):
        """JSON test with all possible update attrs"""
        expected_json_output = (
            '{"subnet": {"gateway_ip": "test_gateway_ip", "host_routes": '
            '[{"route1_key2": "route1_value2", "route1_key": "route1_value"},'
            ' {"route2_key2": "route2_value2", "route2_key": "route2_value"}],'
            ' "name": "test_subnet_name", "enable_dhcp": true, '
            '"dns_nameservers": ["test_dnsname1", "test_dnsname2", '
            '"test_dnsname3"]}}')
        request_body = self.subnet_model._obj_to_json()
        msg = ('Unexpected JSON Subnet request serialization. Expected {0} '
               'instead of {1}'.format(expected_json_output, request_body))
        self.assertEqual(request_body, expected_json_output, msg)


class ShowSubnetTest(unittest.TestCase):
    """Test for the Subnet Show (GET) Model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating subnet_model with currently supported attributes"""
        show_attrs = dict(
            name='my_subnet', enable_dhcp=True,
            network_id='d32019d3-bc6e-4319-9c1d-6722fc136a22',
            tenant_id='4fd44f30292945e481c7b8a0c8908869', dns_nameservers=[],
            allocation_pools=[{u'start': u'192.0.0.2', u'end':
            u'192.255.255.254'}], gateway_ip='192.0.0.1', ip_version=4,
            host_routes=[], cidr='192.0.0.0/8',
            id_='54d6f61d-db07-451c-9ab3-b9609b6b6f0b')
        cls.expected_response = Subnet(**show_attrs)

    def test_json_response(self):
        api_json_resp = (
            """{
                "subnet": {
                    "name": "my_subnet",
                    "enable_dhcp": true,
                    "network_id": "d32019d3-bc6e-4319-9c1d-6722fc136a22",
                    "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
                    "dns_nameservers": [],
                    "allocation_pools": [
                        {
                            "start": "192.0.0.2",
                            "end": "192.255.255.254"
                        }
                    ],
                    "host_routes": [],
                    "ip_version": 4,
                    "gateway_ip": "192.0.0.1",
                    "cidr": "192.0.0.0/8",
                    "id": "54d6f61d-db07-451c-9ab3-b9609b6b6f0b"
                }
            }""")
        response_obj = Subnet()._json_to_obj(api_json_resp)
        self.assertEqual(response_obj, self.expected_response,
                         'JSON to Obj response different than expected')


class ShowMultipleSubnetTest(unittest.TestCase):
    """Test for the Subnet List (GET) Model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating subnet_model with currently supported attributes"""
        show_attrs_1 = dict(
            name='private-subnet', enable_dhcp=True,
            network_id='db193ab3-96e3-4cb3-8fc5-05f4296d0324',
            tenant_id='26a7980765d0414dbc1fc1f88cdb7e6e', dns_nameservers=[],
            allocation_pools=[{u'start': u'10.0.0.2', u'end': u'10.0.0.254'}],
            gateway_ip='10.0.0.1', ip_version=4, host_routes=[],
            cidr='10.0.0.0/24', id_='08eae331-0402-425a-923c-34f7cfe39c1b')
        show_attrs_2 = dict(
            name='my_subnet', enable_dhcp=True,
            network_id='d32019d3-bc6e-4319-9c1d-6722fc136a22',
            tenant_id='4fd44f30292945e481c7b8a0c8908869', dns_nameservers=[],
            allocation_pools=[{u'start': u'192.0.0.2', u'end':
            u'192.255.255.254'}], gateway_ip='192.0.0.1', ip_version=4,
            host_routes=[], cidr='192.0.0.0/8',
            id_='54d6f61d-db07-451c-9ab3-b9609b6b6f0b')
        sub1 = Subnet(**show_attrs_1)
        sub2 = Subnet(**show_attrs_2)
        cls.expected_response = [sub1, sub2]

    def test_json_response(self):
        # Response data with extension attributes, if supported later on they
        # will need to be added to the setUp object model in this test class
        api_json_resp = (
            """{
                "subnets": [
                    {
                        "name": "private-subnet",
                        "enable_dhcp": true,
                        "network_id": "db193ab3-96e3-4cb3-8fc5-05f4296d0324",
                        "tenant_id": "26a7980765d0414dbc1fc1f88cdb7e6e",
                        "dns_nameservers": [],
                        "allocation_pools": [
                            {
                                "start": "10.0.0.2",
                                "end": "10.0.0.254"
                            }
                        ],
                        "host_routes": [],
                        "ip_version": 4,
                        "gateway_ip": "10.0.0.1",
                        "cidr": "10.0.0.0/24",
                        "id": "08eae331-0402-425a-923c-34f7cfe39c1b"
                    },
                    {
                        "name": "my_subnet",
                        "enable_dhcp": true,
                        "network_id": "d32019d3-bc6e-4319-9c1d-6722fc136a22",
                        "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
                        "dns_nameservers": [],
                        "allocation_pools": [
                            {
                                "start": "192.0.0.2",
                                "end": "192.255.255.254"
                            }
                        ],
                        "host_routes": [],
                        "ip_version": 4,
                        "gateway_ip": "192.0.0.1",
                        "cidr": "192.0.0.0/8",
                        "id": "54d6f61d-db07-451c-9ab3-b9609b6b6f0b"
                    }
                ]
            }""")
        response_obj = Subnets()._json_to_obj(api_json_resp)
        self.assertEqual(response_obj, self.expected_response,
                         'JSON to Obj response different than expected')


if __name__ == "__main__":
    unittest.main()
