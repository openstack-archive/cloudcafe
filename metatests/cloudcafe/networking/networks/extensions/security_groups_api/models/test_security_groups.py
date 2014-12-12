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

from cloudcafe.networking.networks.extensions.security_groups_api.models.\
    request import SecurityGroupRequest, SecurityGroupRuleRequest
from cloudcafe.networking.networks.extensions.security_groups_api.models.\
    response import SecurityGroup, SecurityGroups, SecurityGroupRule, \
    SecurityGroupRules


SECURITY_GROUP_TAG = SecurityGroup.SECURITY_GROUP
SECURITY_GROUPS_TAG = SecurityGroups.SECURITY_GROUPS
SECURITY_GROUP_RULE_TAG = SecurityGroupRule.SECURITY_GROUP_RULE
SECURITY_GROUP_RULES_TAG = SecurityGroupRules.SECURITY_GROUP_RULES

SECURITY_GROUP_RULES_DATA = (
    """
    [{
    "direction": "egress",
    "ethertype": "IPv4",
    "id": "38ce2d8e-e8f1-48bd-83c2-d33cb9f50c3d",
    "port_range_max": null,
    "port_range_min": null,
    "protocol": null,
    "remote_group_id": null,
    "remote_ip_prefix": null,
    "security_group_id": "2076db17-a522-4506-91de-c6dd8e837028",
    "tenant_id": "e4f50856753b4dc6afee5fa6b9b6c550"
    },
    {
    "direction": "egress",
    "ethertype": "IPv6",
    "id": "565b9502-12de-4ffd-91e9-68885cff6ae1",
    "port_range_max": null,
    "port_range_min": null,
    "protocol": null,
    "remote_group_id": null,
    "remote_ip_prefix": null,
    "security_group_id": "2076db17-a522-4506-91de-c6dd8e837028",
    "tenant_id": "e4f50856753b4dc6afee5fa6b9b6c550"
    }]""")


class CreateSecurityGroupTest(unittest.TestCase):
    """Test for the Security Groups Create (POST) Model object request"""
    @classmethod
    def setUpClass(cls):
        create_attrs = dict(
            name='test_name_value', description='test_description_value',
            tenant_id='test_tenant_id_value')
        cls.security_group_model = SecurityGroupRequest(**create_attrs)

    def test_json_request(self):
        """JSON test with all possible create attrs"""
        expected_json_output = (
            '{{"{tag}": {{"tenant_id": "test_tenant_id_value", "name": '
            '"test_name_value", "description": "test_description_value"}}}}').\
            format(tag=SECURITY_GROUP_TAG)
        request_body = self.security_group_model._obj_to_json()
        msg = ('Unexpected JSON Network request serialization. Expected {0} '
               'instead of {1}'.format(expected_json_output, request_body))
        self.assertEqual(request_body, expected_json_output, msg)


class CreateSecurityGroupRuleTest(unittest.TestCase):
    """Test for the Security Groups Rule Create (POST) Model object request"""
    @classmethod
    def setUpClass(cls):
        create_attrs = dict(
            direction='dir_val', ethertype='eth_val', security_group_id='s_id',
            port_range_min=1, port_range_max=250, protocol='protocol_val',
            remote_group_id='r_id', remote_ip_prefix='prefix_val')
        cls.rules_model = SecurityGroupRuleRequest(**create_attrs)

    def test_json_request(self):
        """JSON test with all possible create attrs"""
        expected_json_output = (
            '{{"{tag}": {{"remote_group_id": "r_id", "direction": '
            '"dir_val", "protocol": "protocol_val", "ethertype": "eth_val", '
            '"port_range_max": 250, "security_group_id": "s_id", '
            '"port_range_min": 1, "remote_ip_prefix": "prefix_val"}}}}').\
            format(tag=SECURITY_GROUP_RULE_TAG)
        request_body = self.rules_model._obj_to_json()
        msg = ('Unexpected JSON Network request serialization. Expected {0} '
               'instead of {1}'.format(expected_json_output, request_body))
        self.assertEqual(request_body, expected_json_output, msg)


class GetSecurityGroupTest(unittest.TestCase):
    """Test for the Security Groups Show (GET) Model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating security groups model"""
        rule1_attrs = dict(
            id_=u'38ce2d8e-e8f1-48bd-83c2-d33cb9f50c3d', direction=u'egress',
            ethertype=u'IPv4',
            security_group_id=u'2076db17-a522-4506-91de-c6dd8e837028',
            tenant_id=u'e4f50856753b4dc6afee5fa6b9b6c550')
        rule2_attrs = dict(
            id_=u'565b9502-12de-4ffd-91e9-68885cff6ae1', direction=u'egress',
            ethertype=u'IPv6',
            security_group_id=u'2076db17-a522-4506-91de-c6dd8e837028',
            tenant_id=u'e4f50856753b4dc6afee5fa6b9b6c550')
        rules = [SecurityGroupRule(**rule1_attrs),
                 SecurityGroupRule(**rule2_attrs)]
        get_attrs = dict(
            name='security_group_name_1',
            description='group text description',
            tenant_id='e4f50856753b4dc6afee5fa6b9b6c550',
            id_='4e8e5957-649f-477b-9e5b-f1f75b21c03c',
            security_group_rules=rules)
        cls.expected_response = SecurityGroup(**get_attrs)

    def test_json_response(self):
        api_json_resp = (
            """{{
            "{tag}": {{
            "description": "group text description",
            "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
            "name": "security_group_name_1",
            "security_group_rules": {rules_data},
            "tenant_id": "e4f50856753b4dc6afee5fa6b9b6c550"}}}}
            """).format(tag=SECURITY_GROUP_TAG,
                        rules_data=SECURITY_GROUP_RULES_DATA)
        response_obj = SecurityGroup()._json_to_obj(api_json_resp)
        self.assertEqual(response_obj, self.expected_response,
                         'JSON to Obj response different than expected')


class GetSecurityGroupRuleTest(unittest.TestCase):
    """Test for the Security Groups Rule Show (GET) Model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating security groups rule model"""
        get_attrs = dict(
            id_=u'3c0e45ff-adaf-4124-b083-bf390e5482ff', direction=u'egress',
            ethertype=u'IPv6',
            security_group_id=u'85cc3048-abc3-43cc-89b3-377341426ac5',
            tenant_id=u'e4f50856753b4dc6afee5fa6b9b6c550')
        cls.expected_response = SecurityGroupRule(**get_attrs)

    def test_json_response(self):
        api_json_resp = (
            """{{
            "{tag}": {{
            "direction": "egress",
            "ethertype": "IPv6",
            "id": "3c0e45ff-adaf-4124-b083-bf390e5482ff",
            "port_range_max": null,
            "port_range_min": null,
            "protocol": null,
            "remote_group_id": null,
            "remote_ip_prefix": null,
            "security_group_id": "85cc3048-abc3-43cc-89b3-377341426ac5",
            "tenant_id": "e4f50856753b4dc6afee5fa6b9b6c550"
            }}}}""").format(tag=SECURITY_GROUP_RULE_TAG)
        response_obj = SecurityGroupRule()._json_to_obj(api_json_resp)
        self.assertEqual(response_obj, self.expected_response,
                         'JSON to Obj response different than expected')


class ListSecurityGroupsTest(unittest.TestCase):
    """Test for the Security Groups List (GET) Model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating security groups model"""
        rule1_attrs = dict(
            id_=u'38ce2d8e-e8f1-48bd-83c2-d33cb9f50c3d', direction=u'egress',
            ethertype=u'IPv4',
            security_group_id=u'2076db17-a522-4506-91de-c6dd8e837028',
            tenant_id=u'e4f50856753b4dc6afee5fa6b9b6c550')
        rule2_attrs = dict(
            id_=u'565b9502-12de-4ffd-91e9-68885cff6ae1', direction=u'egress',
            ethertype=u'IPv6',
            security_group_id=u'2076db17-a522-4506-91de-c6dd8e837028',
            tenant_id=u'e4f50856753b4dc6afee5fa6b9b6c550')
        rules = [SecurityGroupRule(**rule1_attrs),
                 SecurityGroupRule(**rule2_attrs)]
        get1_attrs = dict(
            name='security_group_name_1',
            description='group text description',
            tenant_id='e4f50856753b4dc6afee5fa6b9b6c550',
            id_='4e8e5957-649f-477b-9e5b-f1f75b21c03c',
            security_group_rules=rules)
        get2_attrs = dict(
            name='security_group_name_2',
            description='group 2 text description',
            tenant_id='a_tenant_id',
            id_='a_security_group_id',
            security_group_rules=rules)
        cls.expected_response = [SecurityGroup(**get1_attrs),
                                 SecurityGroup(**get2_attrs)]

    def test_json_response(self):
        api_json_resp = (
            """{{
            "{tag}": [{{
            "description": "group text description",
            "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
            "name": "security_group_name_1",
            "security_group_rules": {rules_data},
            "tenant_id": "e4f50856753b4dc6afee5fa6b9b6c550"}},
                    {{
            "description": "group 2 text description",
            "id": "a_security_group_id",
            "name": "security_group_name_2",
            "security_group_rules": {rules_data},
            "tenant_id": "a_tenant_id"}}]
            }}""").format(tag=SECURITY_GROUPS_TAG,
                          rules_data=SECURITY_GROUP_RULES_DATA)
        response_obj = SecurityGroups()._json_to_obj(api_json_resp)
        self.assertEqual(response_obj, self.expected_response,
                         'JSON to Obj response different than expected')


class ListSecurityGroupRulesTest(unittest.TestCase):
    """Test for the Security Groups List (GET) Model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating security groups model"""
        rule1_attrs = dict(
            id_=u'38ce2d8e-e8f1-48bd-83c2-d33cb9f50c3d', direction=u'egress',
            ethertype=u'IPv4',
            security_group_id=u'2076db17-a522-4506-91de-c6dd8e837028',
            tenant_id=u'e4f50856753b4dc6afee5fa6b9b6c550')
        rule2_attrs = dict(
            id_=u'565b9502-12de-4ffd-91e9-68885cff6ae1', direction=u'egress',
            ethertype=u'IPv6',
            security_group_id=u'2076db17-a522-4506-91de-c6dd8e837028',
            tenant_id=u'e4f50856753b4dc6afee5fa6b9b6c550')
        cls.expected_response = [SecurityGroupRule(**rule1_attrs),
                 SecurityGroupRule(**rule2_attrs)]

    def test_json_response(self):
        api_json_resp = (
            """{{
            "{tag}": {rules_data}
            }}""").format(tag=SECURITY_GROUP_RULES_TAG,
                          rules_data=SECURITY_GROUP_RULES_DATA)
        response_obj = SecurityGroupRules()._json_to_obj(api_json_resp)
        self.assertEqual(response_obj, self.expected_response,
                         'JSON to Obj response different than expected')


if __name__ == "__main__":
    unittest.main()
