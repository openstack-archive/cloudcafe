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

from cloudcafe.networking.networks.common.models.request.network \
    import NetworkRequest
from cloudcafe.networking.networks.common.models.response.network \
    import Network, Networks

NETWORK_TAG = Network.NETWORK
NETWORKS_TAG = Networks.NETWORKS


class CreateNetworkTest(unittest.TestCase):
    """Test for the Network Create (POST) Model object requests"""
    @classmethod
    def setUpClass(cls):
        create_attrs = dict(
            name='test_name_value', admin_state_up='test_admin_state_up_value',
            shared='test_shared_value', tenant_id='test_tenant_id_value')
        cls.network_model = NetworkRequest(**create_attrs)

    def test_json_request(self):
        """JSON test with all possible create attrs"""
        expected_json_output = (
            '{{"{tag}": {{"shared": "test_shared_value", '
            '"tenant_id": "test_tenant_id_value", "name": "test_name_value", '
            '"admin_state_up": "test_admin_state_up_value"}}}}').format(
            tag=NETWORK_TAG)
        request_body = self.network_model._obj_to_json()
        msg = ('Unexpected JSON Network request serialization. Expected {0} '
               'instead of {1}'.format(expected_json_output, request_body))
        self.assertEqual(request_body, expected_json_output, msg)


class UpdateNetworkTest(unittest.TestCase):
    """Test for the Network Update (PUT) Model object requests"""
    @classmethod
    def setUpClass(cls):
        update_attrs = dict(
            name='test_name_value', admin_state_up='test_admin_state_up_value',
            shared='test_shared_value')
        cls.network_model = NetworkRequest(**update_attrs)

    def test_json_request(self):
        """JSON test with all possible update attrs"""
        expected_json_output = (
            '{{"{tag}": {{"shared": "test_shared_value", '
            '"name": "test_name_value", '
            '"admin_state_up": "test_admin_state_up_value"}}}}').format(
                tag=NETWORK_TAG)
        request_body = self.network_model._obj_to_json()
        msg = ('Unexpected JSON Network request serialization. Expected {0} '
               'instead of {1}'.format(expected_json_output, request_body))
        self.assertEqual(request_body, expected_json_output, msg)


class ShowNetworkTest(unittest.TestCase):
    """Test for the Network Show (GET) Model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating network_model with currently supported attributes"""
        show_attrs = dict(
            status='ACTIVE', subnets=['54d6f61d-db07-451c-9ab3-b9609b6b6f0b',
                                      '79d6f61d-d007-51cd-9a33-b9609b6b6f0c'],
            name='net1', admin_state_up=True,
            tenant_id='9bacb3c5d39d41a79512987f338cf177', shared=False,
            id_='4e8e5957-649f-477b-9e5b-f1f75b21c03c', router_external=True)
        cls.expected_response = Network(**show_attrs)

    def test_json_response(self):
        # Response data with extension attributes, if supported later on they
        # will need to be added to the setUp object model in this test class
        api_json_resp = (
            """{{
                "{tag}": {{
                    "status": "ACTIVE",
                    "subnets": [
                        "54d6f61d-db07-451c-9ab3-b9609b6b6f0b",
                        "79d6f61d-d007-51cd-9a33-b9609b6b6f0c"
                    ],
                    "name": "net1",
                    "admin_state_up": true,
                    "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
                    "segments": [
                        {{
                            "provider:segmentation_id": 2,
                            "provider:physical_network":
                                "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                            "provider:network_type": "vlan"
                        }},
                        {{
                            "provider:segmentation_id": null,
                            "provider:physical_network":
                                "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                            "provider:network_type": "stt"
                        }}
                    ],
                    "shared": false,
                    "port_security_enabled": true,
                    "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
                    "router:external": true
                }}
            }}""").format(tag=NETWORK_TAG)
        response_obj = Network()._json_to_obj(api_json_resp)
        self.assertEqual(response_obj, self.expected_response,
                         'JSON to Obj response different than expected')


class ShowMultipleNetworksTest(unittest.TestCase):
    """Test for the Networks List (GET) Model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating network_model with currently supported attributes"""
        show_attrs_1 = dict(
            status='ACTIVE', subnets=['54d6f61d-db07-451c-9ab3-b9609b6b6f0b'],
            name='private-network', admin_state_up=True,
            tenant_id='4fd44f30292945e481c7b8a0c8908869', shared=True,
            id_='d32019d3-bc6e-4319-9c1d-6722fc136a22', router_external=True)
        show_attrs_2 = dict(
            status='ACTIVE', subnets=['08eae331-0402-425a-923c-34f7cfe39c1b'],
            name='private', admin_state_up=True,
            tenant_id='26a7980765d0414dbc1fc1f88cdb7e6e', shared=True,
            id_='db193ab3-96e3-4cb3-8fc5-05f4296d0324', router_external=True)
        net1 = Network(**show_attrs_1)
        net2 = Network(**show_attrs_2)
        cls.expected_response = [net1, net2]

    def test_json_response(self):
        # Response data with extension attributes, if supported later on they
        # will need to be added to the setUp object model in this test class
        api_json_resp = (
            """{{
                "{tag}": [
                    {{
                        "status": "ACTIVE",
                        "subnets": [
                            "54d6f61d-db07-451c-9ab3-b9609b6b6f0b"
                        ],
                        "name": "private-network",
                        "provider:physical_network": null,
                        "admin_state_up": true,
                        "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
                        "provider:network_type": "local",
                        "router:external": true,
                        "shared": true,
                        "id": "d32019d3-bc6e-4319-9c1d-6722fc136a22",
                        "provider:segmentation_id": null
                    }},
                    {{
                        "status": "ACTIVE",
                        "subnets": [
                            "08eae331-0402-425a-923c-34f7cfe39c1b"
                        ],
                        "name": "private",
                        "provider:physical_network": null,
                        "admin_state_up": true,
                        "tenant_id": "26a7980765d0414dbc1fc1f88cdb7e6e",
                        "provider:network_type": "local",
                        "router:external": true,
                        "shared": true,
                        "id": "db193ab3-96e3-4cb3-8fc5-05f4296d0324",
                        "provider:segmentation_id": null
                    }}
                ]
            }}""").format(tag=NETWORKS_TAG)
        response_obj = Networks()._json_to_obj(api_json_resp)
        self.assertEqual(response_obj, self.expected_response,
                         'JSON to Obj response different than expected')


if __name__ == "__main__":
    unittest.main()
