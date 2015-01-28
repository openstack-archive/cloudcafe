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

@summary: Unit tests for the load balancer Member request models.

CreateMemberRequestTest
UpdateMemberRequestTest
"""

import json
import unittest

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.member.request import \
    CreateMember, UpdateMember


class MemberRequestTestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.XML_HEADER = Constants.XML_HEADER
        cls.XML_NS = Constants.XML_API_NAMESPACE
        cls.subnet_id = "SUBNET_ID"
        cls.tenant_id = "453105b9-1754-413f-aab1-55f1af620750"
        cls.address = "192.0.2.14"
        cls.protocol_port = 8080
        cls.weight = 7
        cls.admin_state_up = True
        cls.create_member_obj = CreateMember(
            subnet_id=cls.subnet_id,
            tenant_id=cls.tenant_id,
            address=cls.address,
            protocol_port=cls.protocol_port,
            weight=cls.weight,
            admin_state_up=cls.admin_state_up,
        )

        cls.updated_weight = 9
        cls.updated_admin_state_up = False
        cls.update_member_obj = UpdateMember(
            weight=cls.updated_weight,
            admin_state_up=cls.updated_admin_state_up
        )


class CreateMemberRequestTest(MemberRequestTestBase):

    def setUp(self):
        self.ROOT_TAG = CreateMember.ROOT_TAG

    def test_create_member_json(self):
        actual_json = json.loads(
            self.create_member_obj.serialize('json'))

        # Create python dict then JSON transform to handle
        # JSON objects and types such as the boolean
        json_dict = {self.ROOT_TAG: {"subnet_id": self.subnet_id,
                                     "tenant_id": self.tenant_id,
                                     "address": self.address,
                                     "protocol_port": self.protocol_port,
                                     "weight": self.weight,
                                     "admin_state_up": self.admin_state_up}}
        expected_json = json.loads(json.dumps(json_dict))
        self.assertEqual(expected_json, actual_json)

    def test_create_member_xml(self):
        actual_xml = self.create_member_obj.serialize('xml')
        expected_xml = (
            '{xml_header}<{root_tag} '
            'address="{address}" '
            'admin_state_up="{admin_state_up}" '
            'protocol_port="{protocol_port}" '
            'subnet_id="{subnet_id}" '
            'tenant_id="{tenant_id}" '
            'weight="{weight}" '
            'xmlns="{xmlns}" />').format(
                xml_header=self.XML_HEADER,
                xmlns=self.XML_NS,
                root_tag=self.ROOT_TAG,
                admin_state_up=str(self.admin_state_up),
                address=self.address,
                protocol_port=str(self.protocol_port),
                subnet_id=self.subnet_id,
                tenant_id=self.tenant_id,
                weight=str(self.weight))
        self.assertEqual(expected_xml, actual_xml)


class UpdateMemberRequestTest(MemberRequestTestBase):

    def setUp(self):
        self.ROOT_TAG = UpdateMember.ROOT_TAG

    def test_update_member_json(self):
        actual_json = json.loads(
            self.update_member_obj.serialize('json'))
        json_dict = {self.ROOT_TAG: {
            "weight": self.updated_weight,
            "admin_state_up": self.updated_admin_state_up}}
        expected_json = json.loads(json.dumps(json_dict))
        self.assertEqual(expected_json, actual_json)

    def test_update_member_xml(self):
        actual_xml = self.update_member_obj.serialize('xml')
        expected_xml = ('{xml_header}<{root_tag} '
                        'admin_state_up="{admin_state_up}" '
                        'weight="{weight}" '
                        'xmlns="{xmlns}" />').format(
                            xml_header=self.XML_HEADER,
                            xmlns=self.XML_NS,
                            root_tag=self.ROOT_TAG,
                            admin_state_up=str(self.updated_admin_state_up),
                            weight=self.updated_weight)
        self.assertEqual(expected_xml, actual_xml)

if __name__ == "__main__":
    unittest.main()
