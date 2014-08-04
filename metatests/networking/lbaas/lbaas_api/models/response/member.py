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

@summary: Unit tests for the load balancer "member" response model.

MemberResponseTest
MembersResponseTest

"""

import unittest

from cloudcafe.networking.lbaas.common.constants import Constants
from cloudcafe.networking.lbaas.lbaas_api.models.response.member \
    import Member, Members


class BaseMemberResponseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseMemberResponseTest, cls).setUpClass()
        cls.XML_HEADER = Constants.XML_HEADER
        cls.XML_NS = Constants.XML_API_NAMESPACE
        cls.id_ = "8992a43f-83af-4b49-9afd-c2bfbd82d7d7"
        cls.subnet_id = "SUBNET_ID"
        cls.tenant_id = "7725fe12-1c14-4f45-ba8e-44bf01763578"
        cls.address = "192.0.2.14"
        cls.protocol_port = 8080
        cls.weight = 7
        cls.admin_state_up = True
        cls.status = "ACTIVE"

        cls.member_obj = Member(
            id_=cls.id_, subnet_id=cls.subnet_id, tenant_id=cls.tenant_id,
            address=cls.address, protocol_port=cls.protocol_port,
            weight=cls.weight, admin_state_up=cls.admin_state_up,
            status=cls.status)
        member_list = [cls.member_obj]
        cls.members_obj = Members(member_list)

        cls.member_attribute_kwargs = {
            "id_": cls.id_,
            "subnet_id": cls.subnet_id,
            "tenant_id": cls.tenant_id,
            "address": cls.address,
            "protocol_port": cls.protocol_port,
            "weight": cls.weight,
            "admin_state_up": str(cls.admin_state_up).lower(),
            "status": cls.status
        }
        cls.actual_json_base = """
                    "id": "{id_}",
                    "subnet_id":"{subnet_id}",
                    "tenant_id":"{tenant_id}",
                    "address": "{address}",
                    "protocol_port": {protocol_port},
                    "weight": {weight},
                    "admin_state_up": {admin_state_up},
                    "status": "{status}"
        """.format(**cls.member_attribute_kwargs)

        cls.actual_xml_base = """
                    id="{id_}"
                    subnet_id="{subnet_id}"
                    tenant_id="{tenant_id}"
                    address="{address}"
                    protocol_port="{protocol_port}"
                    weight="{weight}"
                    admin_state_up="{admin_state_up}"
                    status="{status}"
        """.format(**cls.member_attribute_kwargs)


class MemberResponseTest(BaseMemberResponseTest):

    def setUp(self):
        super(MemberResponseTest, self).setUp()
        self.ROOT_TAG = Member.ROOT_TAG
        self.expected_obj = self.member_obj

    def test_member_json(self):
        actual_json = """
            {{ "{root_tag}":
                {{
                    {actual_json_base}
                }}
            }}
            """.format(root_tag=self.ROOT_TAG,
                       actual_json_base=self.actual_json_base,
                       **self.member_attribute_kwargs)
        actual_obj = Member.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)

    def test_member_xml(self):
        actual_xml = """{xml_header}
                            <{root_tag}
                                {actual_xml_base}
                                xmlns="{xmlns}"
                            />""".format(
            xml_header=self.XML_HEADER,
            xmlns=self.XML_NS,
            root_tag=self.ROOT_TAG,
            actual_xml_base=self.actual_xml_base,
            **self.member_attribute_kwargs)
        actual_obj = Member.deserialize(actual_xml, 'xml')
        self.assertEqual(self.expected_obj, actual_obj)


class MembersResponseTest(BaseMemberResponseTest):

    def setUp(self):
        super(MembersResponseTest, self).setUp()
        self.ROOT_TAG = Members.ROOT_TAG
        self.CHILD_TAG = Member.ROOT_TAG
        self.expected_obj = self.members_obj

    def test_members_json(self):
        actual_json = """
                        {{ "{root_tag}":
                            [{{
                                {actual_json_base}
                            }}]
                        }}
                        """.format(root_tag=self.ROOT_TAG,
                                   actual_json_base=self.actual_json_base,
                                   **self.member_attribute_kwargs)
        actual_obj = Members.deserialize(actual_json, 'json')
        self.assertEqual(self.expected_obj, actual_obj)

    def test_members_xml(self):
        actual_xml = """{xml_header}
                            <{root_tag} xmlns="{xmlns}">
                                <{child_tag}
                                    {actual_xml_base}
                                />
                            </{root_tag}>""".format(
            xml_header=self.XML_HEADER,
            xmlns=self.XML_NS,
            root_tag=self.ROOT_TAG,
            child_tag=self.CHILD_TAG,
            actual_xml_base=self.actual_xml_base,
            **self.member_attribute_kwargs)
        actual_obj = Members.deserialize(actual_xml, 'xml')
        self.assertEqual(self.expected_obj, actual_obj)


if __name__ == "__main__":
    unittest.main()
