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

@summary: Unit tests for the load balancer request models.

CreateLoadBalancerRequestTest
UpdateLoadBalancerRequestTest
"""

import json
import unittest2 as unittest

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.models.request.load_balancer import \
    CreateLoadBalancer, UpdateLoadBalancer


class LoadBalancerRequestTestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.XML_HEADER = Constants.XML_HEADER
        cls.name = "a-new-loadbalancer"
        cls.vip_subnet = "SUBNET_ID"
        cls.tenant_id = "7725fe12-1c14-4f45-ba8e-44bf01763578"
        cls.admin_state_up = True
        cls.description = "A very simple example load balancer."
        cls.vip_address = "1.2.3.4"

        cls.create_load_balancer_obj = CreateLoadBalancer(
            name=cls.name,
            vip_subnet=cls.vip_subnet,
            tenant_id=cls.tenant_id,
            admin_state_up=cls.admin_state_up,
            description=cls.description,
            vip_address=cls.vip_address
        )

        cls.updated_name = "an_updated-loadbalancer"
        cls.updated_description = "An updated simple example load balancer."
        cls.updated_admin_state_up = False
        cls.update_load_balancer_obj = UpdateLoadBalancer(
            name=cls.updated_name,
            description=cls.updated_description,
            admin_state_up=cls.updated_admin_state_up
        )


class CreateLoadBalancerRequestTest(LoadBalancerRequestTestBase):

    def setUp(self):
        self.ROOT_TAG = CreateLoadBalancer.ROOT_TAG

    def test_create_load_balancer_json(self):
        actual_json = json.loads(
            self.create_load_balancer_obj.serialize('json'))

        # Create python dict then JSON transform to handle
        # JSON objects and types such as the boolean
        json_dict = {self.ROOT_TAG: {"name": self.name,
                                     "description": self.description,
                                     "vip_subnet": self.vip_subnet,
                                     "vip_address": self.vip_address,
                                     "tenant_id": self.tenant_id,
                                     "admin_state_up": self.admin_state_up}}
        expected_json = json.loads(json.dumps(json_dict))
        self.assertEqual(expected_json, actual_json)

    def test_create_load_balancer_xml(self):
        actual_xml = self.create_load_balancer_obj.serialize('xml')
        expected_xml = (
            '{xml_header}<{root_tag} '
            'admin_state_up="{admin_state_up}" '
            'description="{description}" '
            'name="{name}" '
            'tenant_id="{tenant_id}" '
            'vip_address="{vip_address}" '
            'vip_subnet="{vip_subnet}" '
            'xmlns="{xmlns}" />').format(
                xml_header=self.XML_HEADER,
                xmlns=Constants.XML_API_NAMESPACE,
                root_tag=self.ROOT_TAG,
                name=self.name, description=self.description,
                vip_subnet=self.vip_subnet, vip_address=self.vip_address,
                tenant_id=self.tenant_id,
                admin_state_up=str(self.admin_state_up))
        self.assertEqual(expected_xml, actual_xml)


class UpdateLoadBalancerRequestTest(LoadBalancerRequestTestBase):

    def setUp(self):
        self.ROOT_TAG = UpdateLoadBalancer.ROOT_TAG

    def test_update_load_balancer_json(self):
        actual_json = json.loads(
            self.update_load_balancer_obj.serialize('json'))
        json_dict = {self.ROOT_TAG: {
            "name": self.updated_name,
            "description": self.updated_description,
            "admin_state_up": self.updated_admin_state_up}}
        expected_json = json.loads(json.dumps(json_dict))
        self.assertEqual(expected_json, actual_json)

    def test_update_load_balancer_xml(self):
        actual_xml = self.update_load_balancer_obj.serialize('xml')
        expected_xml = ('{xml_header}<{root_tag} '
                        'admin_state_up="{admin_state_up}" '
                        'description="{description}" '
                        'name="{name}" '
                        'xmlns="{xmlns}" />').format(
                            xml_header=self.XML_HEADER,
                            xmlns=Constants.XML_API_NAMESPACE,
                            root_tag=self.ROOT_TAG,
                            name=self.updated_name,
                            description=self.updated_description,
                            admin_state_up=str(self.updated_admin_state_up))
        self.assertEqual(expected_xml, actual_xml)

if __name__ == "__main__":
    unittest.main()
