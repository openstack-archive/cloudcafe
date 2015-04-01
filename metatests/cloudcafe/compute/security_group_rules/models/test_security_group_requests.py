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

import unittest

from cloudcafe.compute.extensions.security_groups_api.models.\
    requests import CreateSecurityGroupRule


class CreateSecurityGroupRuleRequestTest(unittest.TestCase):

    def test_serialize_create_security_group_rule_request_to_json(self):
        create_sec_group_rule_obj = CreateSecurityGroupRule(ip_protocol="tcp",
                                                            from_port=80,
                                                            to_port=8080,
                                                            cidr="0.0.0.0/0",
                                                            group_id=1,
                                                            parent_group_id=2)
        json_serialized_obj = create_sec_group_rule_obj.serialize("json")
        expected_json = ('{"security_group_rule":'
                         ' {"from_port": 80,'
                         ' "ip_protocol": "tcp",'
                         ' "to_port": 8080,'
                         ' "parent_group_id": 2,'
                         ' "cidr": "0.0.0.0/0",'
                         ' "group_id": 1}}')
        self.assertEqual(json_serialized_obj, expected_json)

    def test_serialize_host_update_request_to_xml(self):
        create_sec_group_rule_obj = CreateSecurityGroupRule(ip_protocol="tcp",
                                                            from_port=80,
                                                            to_port=8080,
                                                            cidr="0.0.0.0/0",
                                                            group_id=1,
                                                            parent_group_id=2)
        xml_serialized_obj = create_sec_group_rule_obj.serialize("xml")
        expected_xml = ('<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
                        '<security_group_rule>'
                        '<from_port>80</from_port>'
                        '<ip_protocol>tcp</ip_protocol>'
                        '<to_port>8080</to_port>'
                        '<parent_group_id>2</parent_group_id>'
                        '<cidr>0.0.0.0/0</cidr>'
                        '<group_id>1</group_id>'
                        '</security_group_rule>')
        self.assertEqual(xml_serialized_obj, expected_xml)
