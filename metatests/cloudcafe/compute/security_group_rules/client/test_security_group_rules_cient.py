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

from httpretty import HTTPretty

from cloudcafe.compute.extensions.security_groups_api.client\
    import SecurityGroupRulesClient
from metatests.cloudcafe.compute.fixtures \
    import ClientTestFixture
from metatests.cloudcafe.compute.security_group_rules.\
    client.responses import SecurityGroupRulesMockResponse


class SecurityGroupRulesClientTest(ClientTestFixture):

    @classmethod
    def setUpClass(cls):
        super(SecurityGroupRulesClientTest, cls).setUpClass()
        cls.security_groups_client = SecurityGroupRulesClient(
            url=cls.COMPUTE_API_ENDPOINT,
            auth_token=cls.AUTH_TOKEN,
            serialize_format=cls.FORMAT,
            deserialize_format=cls.FORMAT)
        cls.security_group_rules_uri = "{0}/os-security-group-rules".\
            format(cls.COMPUTE_API_ENDPOINT)
        cls.mock_response = SecurityGroupRulesMockResponse(cls.FORMAT)

    def test_create_security_group_rule(self):
        HTTPretty.register_uri(HTTPretty.POST, self.security_group_rules_uri,
                               body=self.mock_response._get_sec_group_rule())
        expected_request_body = '{"security_group_rule":' \
                                ' {"from_port": 80,' \
                                ' "ip_protocol": "tcp",' \
                                ' "to_port": 8080,' \
                                ' "parent_group_id": 2,' \
                                ' "cidr": "0.0.0.0/0",' \
                                ' "group_id": 1}}'
        actual_response = self.security_groups_client.\
            create_rule(from_port=80, ip_protocol="tcp",
                        to_port=8080, parent_group_id=2,
                        cidr="0.0.0.0/0", group_id=1)
        self._assert_default_headers_in_request(HTTPretty.last_request)
        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(HTTPretty.last_request.body, expected_request_body)
        self.assertEqual(self.mock_response._get_sec_group_rule(),
                         actual_response.content)
