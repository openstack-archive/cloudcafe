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

@summary: Unit tests for the load balancer "listener" request model.

CreateListenerRequestTest
UpdateListenerRequestTest
"""

import json
import unittest

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.listener.request import \
    CreateListener, UpdateListener


class ListenerRequestTestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.XML_HEADER = Constants.XML_HEADER
        cls.XML_NS = Constants.XML_API_NAMESPACE
        cls.name = "Example HTTPS Listener"
        cls.load_balancer_id = "b8a35470-f65d-11e3-a3ac-0800200c9a66"
        cls.tenant_id = "352686b7-c4b2-44ec-a458-84239713f685"
        cls.default_pool_id = "8311446e-8a13-4c00-95b3-03a92f9759c7"
        cls.protocol = "https"
        cls.protocol_port = 443
        cls.description = "A very simple example of an HTTPS listener."
        cls.connection_limit = 200
        cls.admin_state_up = True

        cls.create_listener_obj = CreateListener(
            name=cls.name,
            load_balancer_id=cls.load_balancer_id,
            tenant_id=cls.tenant_id,
            default_pool_id=cls.default_pool_id,
            protocol=cls.protocol,
            protocol_port=cls.protocol_port,
            description=cls.description,
            connection_limit=cls.connection_limit,
            admin_state_up=cls.admin_state_up
        )

        cls.updated_name = "Updated Example HTTPS Listener"
        cls.updated_description = "A updated example of an HTTPS listener."
        cls.updated_default_pool_id = "updated-8a13-4c00-95b3-03a92f9759c7"
        cls.updated_load_balancer_id = "updated-f65d-11e3-a3ac-0800200c9a66"
        cls.updated_admin_state_up = False

        cls.update_listener_obj = UpdateListener(
            name=cls.updated_name,
            description=cls.updated_description,
            load_balancer_id=cls.updated_load_balancer_id,
            default_pool_id=cls.updated_default_pool_id,
            admin_state_up=cls.updated_admin_state_up
        )


class CreateListenerRequestTest(ListenerRequestTestBase):

    def setUp(self):
        self.ROOT_TAG = CreateListener.ROOT_TAG

    def test_create_listener_json(self):
        actual_json = json.loads(self.create_listener_obj.serialize('json'))

        # Create python dict then JSON transform to handle
        # JSON objects and types such as the boolean
        json_dict = {self.ROOT_TAG: {'name': self.name,
                                     'load_balancer_id': self.load_balancer_id,
                                     'tenant_id': self.tenant_id,
                                     'default_pool_id': self.default_pool_id,
                                     'protocol': self.protocol,
                                     'protocol_port': self.protocol_port,
                                     'description': self.description,
                                     'connection_limit': self.connection_limit,
                                     'admin_state_up': self.admin_state_up}}
        expected_json = json.loads(json.dumps(json_dict))
        self.assertEqual(expected_json, actual_json)

    def test_create_listener_xml(self):
        actual_xml = self.create_listener_obj.serialize('xml')
        expected_xml = (
            '{xml_header}<{root_tag} '
            'admin_state_up="{admin_state_up}" '
            'connection_limit="{connection_limit}" '
            'default_pool_id="{default_pool_id}" '
            'description="{description}" '
            'load_balancer_id="{load_balancer_id}" '
            'name="{name}" '
            'protocol="{protocol}" '
            'protocol_port="{protocol_port}" '
            'tenant_id="{tenant_id}" xmlns="{xmlns}" />').format(
                xml_header=self.XML_HEADER,
                xmlns=self.XML_NS,
                root_tag=self.ROOT_TAG,
                name=self.name, load_balancer_id=self.load_balancer_id,
                tenant_id=self.tenant_id, default_pool_id=self.default_pool_id,
                protocol=self.protocol, protocol_port=self.protocol_port,
                description=self.description,
                connection_limit=self.connection_limit,
                admin_state_up=self.admin_state_up)
        self.assertEqual(expected_xml, actual_xml)


class UpdateListenerRequestTest(ListenerRequestTestBase):

    def setUp(self):
        self.ROOT_TAG = UpdateListener.ROOT_TAG

    def test_update_listener_json(self):
        actual_json = json.loads(
            self.update_listener_obj.serialize('json'))
        json_dict = {self.ROOT_TAG: {
            "name": self.updated_name,
            "description": self.updated_description,
            "default_pool_id": self.updated_default_pool_id,
            "load_balancer_id": self.updated_load_balancer_id,
            "admin_state_up": self.updated_admin_state_up}}
        expected_json = json.loads(json.dumps(json_dict))
        self.assertEqual(expected_json, actual_json)

    def test_update_listener_xml(self):
        actual_xml = self.update_listener_obj.serialize('xml')
        expected_xml = ('{xml_header}<{root_tag} '
                        'admin_state_up="{admin_state_up}" '
                        'default_pool_id="{default_pool_id}" '
                        'description="{description}" '
                        'load_balancer_id="{load_balancer_id}" '
                        'name="{name}" '
                        'xmlns="{xmlns}" />').format(
                            xml_header=self.XML_HEADER,
                            xmlns=self.XML_NS,
                            root_tag=self.ROOT_TAG,
                            name=self.updated_name,
                            description=self.updated_description,
                            default_pool_id=self.updated_default_pool_id,
                            load_balancer_id=self.updated_load_balancer_id,
                            admin_state_up=str(self.updated_admin_state_up))
        self.assertEqual(expected_xml, actual_xml)

if __name__ == "__main__":
    unittest.main()
