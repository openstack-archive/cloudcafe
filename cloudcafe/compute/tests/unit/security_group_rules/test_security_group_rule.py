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

import unittest2 as unittest

from cloudcafe.compute.extensions.security_groups_api.models.\
    security_group_rule import SecurityGroupRule


class SecurityGroupRuleDomainTest(object):

    def test_security_group_rule_attributes(self):
        self.assertEqual(str(self.sec_group_rule.from_port), '80')
        self.assertEqual(str(self.sec_group_rule.to_port), '8080')
        self.assertEqual(self.sec_group_rule.ip_protocol, 'tcp')
        self.assertEqual(self.sec_group_rule.id,
                         'bf57c853-cdf2-4c99-9f9a-79b3e9dc13a8')
        self.assertEqual(self.sec_group_rule.parent_group_id,
                         'b32c047d-5efc-42ab-8476-3ac9f3681af2')
        self.assertEqual(self.sec_group_rule.ip_range.cidr, '0.0.0.0/0')


class SecurityGroupRuleDomainJSONTest(unittest.TestCase,
                                      SecurityGroupRuleDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.sec_group_rule_json = '{"security_group_rule":' \
                                  ' {"from_port": 80,' \
                                  '"group": {},' \
                                  '"ip_protocol": "tcp",' \
                                  '"to_port": 8080,' \
                                  '"parent_group_id":' \
                                  ' "b32c047d-5efc-42ab-8476-3ac9f3681af2",' \
                                  '"ip_range": {"cidr": "0.0.0.0/0"},' \
                                  '"id":' \
                                  ' "bf57c853-cdf2-4c99-9f9a-79b3e9dc13a8"}}'
        cls.sec_group_rule = SecurityGroupRule.\
            deserialize(cls.sec_group_rule_json, "json")


class SecurityGroupRuleDomainXMLTest(unittest.TestCase,
                                     SecurityGroupRuleDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.sec_group_rule_xml = '<?xml version="1.0" encoding="UTF-8"?>' \
                                 '<security_group_rule ' \
                                 'xmlns=' \
                                 '"http://docs.openstack.org/' \
                                 'compute/api/v1.1"' \
                                 'parent_group_id=' \
                                 '"b32c047d-5efc-42ab-8476-3ac9f3681af2" ' \
                                 'id=' \
                                 '"bf57c853-cdf2-4c99-9f9a-79b3e9dc13a8">' \
                                 '<ip_protocol>tcp</ip_protocol>' \
                                 '<from_port>80</from_port>' \
                                 '<to_port>8080</to_port>' \
                                 '<group>' \
                                 '<name>None</name>' \
                                 '<tenant_id>None</tenant_id>' \
                                 '</group>' \
                                 '<ip_range>' \
                                 '<cidr>0.0.0.0/0</cidr>' \
                                 '</ip_range>' \
                                 '</security_group_rule>'
        cls.sec_group_rule = SecurityGroupRule.\
            deserialize(cls.sec_group_rule_xml, "xml")

if __name__ == '__main__':
    unittest.main()
