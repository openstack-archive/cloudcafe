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

CreatePoolRequestTest
UpdatePoolRequestTest
"""

import json
import unittest

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.pool.request import \
    CreatePool, UpdatePool


class PoolRequestTestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.XML_HEADER = Constants.XML_HEADER
        cls.XML_NS = Constants.XML_API_NAMESPACE
        cls.name = "Example HTTPS Pool"
        cls.description = "Example HTTPS Pool Description"
        cls.tenant_id = "352686b7-c4b2-44ec-a458-84239713f685"
        cls.protocol = "HTTPS"
        cls.lb_algorithm = "ROUND_ROBIN"
        cls.healthmonitor_id = "health_monitor_123"
        cls.admin_state_up = True
        cls.sp_type = "COOKIE"
        cls.sp_cookie_name = "session_persistence_cookie"
        cls.session_persistence = {"type": cls.sp_type,
                                   "cookie_name": cls.sp_cookie_name}
        cls.create_pool_obj = CreatePool(
            name=cls.name,
            description=cls.description,
            tenant_id=cls.tenant_id,
            protocol=cls.protocol,
            session_persistence=cls.session_persistence,
            lb_algorithm=cls.lb_algorithm,
            healthmonitor_id=cls.healthmonitor_id,
            admin_state_up=cls.admin_state_up
        )

        cls.updated_name = "Updated Example HTTPS Pool"
        cls.updated_description = "A updated example of an HTTPS Pool."
        cls.updated_lb_algorithm = "LEAST_CONNECTIONS"
        cls.updated_healthmonitor_id = "health_monitor_321"
        cls.updated_admin_state_up = False
        cls.updated_sp_type = "SOURCE_IP"
        cls.updated_sp_cookie_name = "updated_session_persistence_cookie"
        cls.updated_session_persistence = {
            "type": cls.updated_sp_type,
            "cookie_name": cls.updated_sp_cookie_name}
        cls.update_pool_obj = UpdatePool(
            name=cls.updated_name,
            description=cls.updated_description,
            lb_algorithm=cls.updated_lb_algorithm,
            healthmonitor_id=cls.updated_healthmonitor_id,
            admin_state_up=cls.updated_admin_state_up,
            session_persistence=cls.updated_session_persistence
        )


class CreatePoolRequestTest(PoolRequestTestBase):

    def setUp(self):
        self.ROOT_TAG = CreatePool.ROOT_TAG

    def test_create_pool_json(self):
        actual_json = json.loads(self.create_pool_obj.serialize('json'))

        # Create python dict then JSON transform to handle
        # JSON objects and types such as the boolean
        json_dict = {self.ROOT_TAG: {
            'name': self.name,
            'tenant_id': self.tenant_id,
            'protocol': self.protocol,
            'lb_algorithm': self.lb_algorithm,
            'description': self.description,
            'session_persistence': self.session_persistence,
            'healthmonitor_id': self.healthmonitor_id,
            'admin_state_up': self.admin_state_up}}
        expected_json = json.loads(json.dumps(json_dict))
        self.assertEqual(expected_json, actual_json)

    def test_create_pool_xml(self):
        actual_xml = self.create_pool_obj.serialize('xml')
        expected_xml = (
            '{xml_header}<{root_tag} '
            'admin_state_up="{admin_state_up}" '
            'description="{description}" '
            'healthmonitor_id="{healthmonitor_id}" '
            'lb_algorithm="{lb_algorithm}" '
            'name="{name}" '
            'protocol="{protocol}" '
            'tenant_id="{tenant_id}" xmlns="{xmlns}">'
            '<session_persistence cookie_name="{sp_cookie_name}" '
            'type="{sp_type}" />'
            '</{root_tag}>').format(
                xml_header=self.XML_HEADER,
                xmlns=self.XML_NS,
                root_tag=self.ROOT_TAG,
                name=self.name, tenant_id=self.tenant_id,
                protocol=self.protocol, lb_algorithm=self.lb_algorithm,
                description=self.description,
                sp_cookie_name=self.sp_cookie_name,
                sp_type=self.sp_type,
                healthmonitor_id=self.healthmonitor_id,
                admin_state_up=self.admin_state_up)
        self.assertEqual(expected_xml, actual_xml)


class UpdatePoolRequestTest(PoolRequestTestBase):

    def setUp(self):
        self.ROOT_TAG = UpdatePool.ROOT_TAG

    def test_update_pool_json(self):
        actual_json = json.loads(
            self.update_pool_obj.serialize('json'))
        json_dict = {self.ROOT_TAG: {
            "name": self.updated_name,
            "description": self.updated_description,
            "session_persistence": self.updated_session_persistence,
            "lb_algorithm": self.updated_lb_algorithm,
            "healthmonitor_id": self.updated_healthmonitor_id,
            "admin_state_up": self.updated_admin_state_up}}
        expected_json = json.loads(json.dumps(json_dict))
        self.assertEqual(expected_json, actual_json)

    def test_update_pool_xml(self):
        actual_xml = self.update_pool_obj.serialize('xml')
        expected_xml = ('{xml_header}<{root_tag} '
                        'admin_state_up="{admin_state_up}" '
                        'description="{description}" '
                        'healthmonitor_id="{healthmonitor_id}" '
                        'lb_algorithm="{lb_algorithm}" '
                        'name="{name}" xmlns="{xmlns}">'
                        '<session_persistence cookie_name="{sp_cookie_name}" '
                        'type="{sp_type}" />'
                        '</{root_tag}>').format(
                            xml_header=self.XML_HEADER,
                            xmlns=self.XML_NS,
                            root_tag=self.ROOT_TAG,
                            admin_state_up=self.updated_admin_state_up,
                            description=self.updated_description,
                            healthmonitor_id=self.updated_healthmonitor_id,
                            lb_algorithm=self.updated_lb_algorithm,
                            name=self.updated_name,
                            sp_cookie_name=self.updated_sp_cookie_name,
                            sp_type=self.updated_sp_type)
        self.assertEqual(expected_xml, actual_xml)

if __name__ == "__main__":
    unittest.main()
