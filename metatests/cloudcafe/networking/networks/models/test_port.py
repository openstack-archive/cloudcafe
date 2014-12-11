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

import unittest

from cloudcafe.networking.networks.common.models.request.port \
    import PortRequest
from cloudcafe.networking.networks.common.models.response.port \
    import Port, Ports

PORT_TAG = Port.PORT
PORTS_TAG = Ports.PORTS


class CreatePortTest(unittest.TestCase):
    """Test for the Port Create (POST) Model object requests"""
    @classmethod
    def setUpClass(cls):
        create_attrs = dict(
            network_id='a87cc70a-3e15-4acf-8205-9b711a3531b7',
            name='private-port', admin_state_up=True)
        cls.subnet_model = PortRequest(**create_attrs)

        # With all possible create attributes
        create_attrs_all = dict(
            network_id='test_net_id', name='port_name', admin_state_up=False,
            mac_address='fa:16:3e:c9:cb:f0', fixed_ips=[{'subnet_id':
            'subnet_id_value', 'ip_address': 'ip_address_value'},
            {'subnet_id2': 'subnet_id_value2', 'ip_address2':
            'ip_address_value2'}], device_id='test_device_id',
            device_owner='test_device_owner', tenant_id='test_tenant_id',
            security_groups=[[{'key1': 'value1', 'key2': 'value2'}, {'key1b':
            'value1b', 'key2b':'value2b'}]])
        cls.subnet_model_all = PortRequest(**create_attrs_all)

    def test_json_request(self):
        """JSON test with create attrs"""
        expected_json_output = (
            '{{"{tag}": {{"network_id": "a87cc70a-3e15-4acf-8205-9b711a3531b7"'
            ', "name": "private-port", "admin_state_up": true}}}}').format(
                tag=PORT_TAG)

        request_body = self.subnet_model._obj_to_json()
        msg = ('Unexpected JSON Port request serialization. Expected {0} '
               'instead of {1}'.format(expected_json_output, request_body))
        self.assertEqual(request_body, expected_json_output, msg)

    def test_json_request_all_attrs(self):
        """JSON test with all create attrs"""
        expected_json_output = (
            '{{"{tag}": {{"name": "port_name", "admin_state_up": false, '
            '"network_id": "test_net_id", "tenant_id": "test_tenant_id", '
            '"device_owner": "test_device_owner", "mac_address": '
            '"fa:16:3e:c9:cb:f0", "fixed_ips": [{{"subnet_id": '
            '"subnet_id_value", "ip_address": "ip_address_value"}}, '
            '{{"subnet_id2": "subnet_id_value2", "ip_address2": '
            '"ip_address_value2"}}], "security_groups": [[{{"key2": "value2", '
            '"key1": "value1"}}, {{"key2b": "value2b", "key1b": "value1b"}}]],'
            ' "device_id": "test_device_id"}}}}').format(tag=PORT_TAG)
        request_body = self.subnet_model_all._obj_to_json()
        msg = ('Unexpected JSON Subnet request serialization. Expected {0} '
               'instead of {1}'.format(expected_json_output, request_body))
        self.assertEqual(request_body, expected_json_output, msg)


class UpdatePortTest(unittest.TestCase):
    """Test for the Port Update (PUT) Model object requests"""
    @classmethod
    def setUpClass(cls):
        update_attrs = dict(
            name='port_update_name', admin_state_up=True,
            fixed_ips=[{'subnet_id': 'subnet_updated_id_value', 'ip_address':
            'ip_address_updated_value'}, {'subnet_id2':
            'subnet_id_updated_value2', 'ip_address2':
            'ip_address_updated_value2'}],
            device_id='updated_device_id', device_owner='updated_device_owner',
            security_groups=[[{'key1': 'updated_value1', 'key2':
            'updated_value2'}, {'key1b': 'updated_value1b', 'key2b':
            'updated_value2b'}]])
        cls.subnet_model = PortRequest(**update_attrs)

    def test_json_request(self):
        """JSON test with all possible update attrs"""
        expected_json_output = (
            '{{"{tag}": {{"name": "port_update_name", "admin_state_up": true, '
            '"device_owner": "updated_device_owner", "fixed_ips": '
            '[{{"subnet_id": "subnet_updated_id_value", "ip_address": '
            '"ip_address_updated_value"}}, {{"subnet_id2": '
            '"subnet_id_updated_value2", "ip_address2": '
            '"ip_address_updated_value2"}}], "security_groups": '
            '[[{{"key2": "updated_value2", "key1": "updated_value1"}}, '
            '{{"key2b": "updated_value2b", "key1b": "updated_value1b"}}]], '
            '"device_id": "updated_device_id"}}}}').format(tag=PORT_TAG)
        request_body = self.subnet_model._obj_to_json()
        msg = ('Unexpected JSON Subnet request serialization. Expected {0} '
               'instead of {1}'.format(expected_json_output, request_body))
        self.assertEqual(request_body, expected_json_output, msg)


class ShowPortTest(unittest.TestCase):
    """Test for the Port Show (GET) Model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating port_model with with extension included attributes"""
        show_attrs = dict(
            status="ACTIVE", name="response_name",
            allowed_address_pairs=[], admin_state_up=True,
            network_id="a87cc70a-3e15-4acf-8205-9b711a3531b7",
            tenant_id="7e02058126cc4950b75f9970368ba177",
            extra_dhcp_opts=[],
            device_owner="network:router_interface",
            mac_address="fa:16:3e:23:fd:d7",
            fixed_ips=[{"subnet_id":
            "a0304c3a-4f08-4c43-88af-d796509c97d2", "ip_address": "10.0.0.1"}],
            id_="46d4bfb9-b26e-41f3-bd2e-e6dcc1ccedb2", security_groups=[],
            device_id="5e3898d7-11be-483e-9732-b2f5eccd2b2e")
        cls.expected_response = Port(**show_attrs)

    def test_json_response(self):
        api_json_resp = (
            """{{
                "{tag}": {{
                    "status": "ACTIVE",
                    "name": "response_name",
                    "allowed_address_pairs": [],
                    "admin_state_up": true,
                    "network_id": "a87cc70a-3e15-4acf-8205-9b711a3531b7",
                    "tenant_id": "7e02058126cc4950b75f9970368ba177",
                    "extra_dhcp_opts": [],
                    "device_owner": "network:router_interface",
                    "mac_address": "fa:16:3e:23:fd:d7",
                    "fixed_ips": [
                        {{
                        "subnet_id": "a0304c3a-4f08-4c43-88af-d796509c97d2",
                        "ip_address": "10.0.0.1"
                        }}
                    ],
                    "id": "46d4bfb9-b26e-41f3-bd2e-e6dcc1ccedb2",
                    "security_groups": [],
                    "device_id": "5e3898d7-11be-483e-9732-b2f5eccd2b2e"
                }}
            }}""").format(tag=PORT_TAG)
        response_obj = Port()._json_to_obj(api_json_resp)
        self.assertEqual(response_obj, self.expected_response,
                         'JSON to Obj response different than expected')


class ShowMultiplePortTest(unittest.TestCase):
    """Test for the Port List (GET) Model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating port_model with currently supported attributes"""
        show_attrs_1 = dict(
            status='ACTIVE', name='', admin_state_up=True,
            network_id='70c1db1f-b701-45bd-96e0-a313ee3430b3', tenant_id='',
            mac_address='fa:16:3e:58:42:ed',
            device_owner='network:router_gateway',
            fixed_ips=[{u'subnet_id': u'008ba151-0b8c-4a67-98b5-0d2b87666062',
            u'ip_address': u'172.24.4.2'}],
            id_='d80b1a3b-4fc1-49f3-952e-1e2ab7081d8b', security_groups=[],
            device_id='9ae135f4-b6e0-4dad-9e91-3c223e385824')
        show_attrs_2 = dict(
            status='ACTIVE', name='', admin_state_up=True,
            network_id='f27aa545-cbdd-4907-b0c6-c9e8b039dcc2',
            tenant_id='d397de8a63f341818f198abb0966f6f3',
            mac_address='fa:16:3e:bb:3c:e4',
            device_owner='network:router_interface', fixed_ips=[{u'subnet_id':
            u'288bf4a1-51ba-43b6-9d0a-520e9005db17', u'ip_address':
            u'10.0.0.1'}], id_='f71a6703-d6de-4be1-a91a-a570ede1d159',
            security_groups=[],
            device_id='9ae135f4-b6e0-4dad-9e91-3c223e385824',)
        sub1 = Port(**show_attrs_1)
        sub2 = Port(**show_attrs_2)
        cls.expected_response = [sub1, sub2]

    def test_json_response(self):
        api_json_resp = (
            """{{
                "{tag}": [
                    {{
                        "status": "ACTIVE",
                        "name": "",
                        "admin_state_up": true,
                        "network_id": "70c1db1f-b701-45bd-96e0-a313ee3430b3",
                        "tenant_id": "",
                        "device_owner": "network:router_gateway",
                        "mac_address": "fa:16:3e:58:42:ed",
                        "fixed_ips": [
                            {{
                        "subnet_id": "008ba151-0b8c-4a67-98b5-0d2b87666062",
                        "ip_address": "172.24.4.2"
                            }}
                        ],
                        "id": "d80b1a3b-4fc1-49f3-952e-1e2ab7081d8b",
                        "security_groups": [],
                        "device_id": "9ae135f4-b6e0-4dad-9e91-3c223e385824"
                    }},
                    {{
                        "status": "ACTIVE",
                        "name": "",
                        "admin_state_up": true,
                        "network_id": "f27aa545-cbdd-4907-b0c6-c9e8b039dcc2",
                        "tenant_id": "d397de8a63f341818f198abb0966f6f3",
                        "device_owner": "network:router_interface",
                        "mac_address": "fa:16:3e:bb:3c:e4",
                        "fixed_ips": [
                            {{
                        "subnet_id": "288bf4a1-51ba-43b6-9d0a-520e9005db17",
                        "ip_address": "10.0.0.1"
                            }}
                        ],
                        "id": "f71a6703-d6de-4be1-a91a-a570ede1d159",
                        "security_groups": [],
                        "device_id": "9ae135f4-b6e0-4dad-9e91-3c223e385824"
                    }}
                ]
            }}""").format(tag=PORTS_TAG)
        response_obj = Ports()._json_to_obj(api_json_resp)
        self.assertEqual(response_obj, self.expected_response,
                         'JSON to Obj response different than expected')


if __name__ == "__main__":
    unittest.main()
