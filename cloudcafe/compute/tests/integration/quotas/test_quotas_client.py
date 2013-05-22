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
from httpretty import HTTPretty
from cloudcafe.compute.quotas_api.client import QuotasClient

from cloudcafe.compute.tests.integration.fixtures import IntegrationTestFixture
from cloudcafe.compute.tests.integration.quotas.responses\
    import QuotasMockResponse


class QuotasClientTest(IntegrationTestFixture):

    @classmethod
    def setUpClass(cls):
        super(QuotasClientTest, cls).setUpClass()
        cls.quotas_client = QuotasClient(
            url=cls.COMPUTE_API_ENDPOINT,
            auth_token=cls.AUTH_TOKEN,
            serialize_format=cls.FORMAT,
            deserialize_format=cls.FORMAT)
        cls.quotas_uri = "{0}/os-quota-sets/{1}".\
            format(cls.COMPUTE_API_ENDPOINT, cls.TENANT_ID)
        cls.default_quotas_uri = "{0}/os-quota-sets/{1}/defaults".\
            format(cls.COMPUTE_API_ENDPOINT, cls.TENANT_ID)
        cls.mock_response = QuotasMockResponse(cls.FORMAT)

    def test_get_quota(self):
        HTTPretty.register_uri(HTTPretty.GET, self.quotas_uri,
                               body=self.mock_response._get_quota())
        actual_response = self.quotas_client.get_quota(self.TENANT_ID)

        self._assert_default_headers_in_request(HTTPretty.last_request)
        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(self.mock_response._get_quota(),
                         actual_response.content)

    def test_get_default_quota(self):
        HTTPretty.register_uri(HTTPretty.GET, self.default_quotas_uri,
                               body=self.mock_response._get_quota())
        actual_response = self.quotas_client.get_default_quota(self.TENANT_ID)

        self._assert_default_headers_in_request(HTTPretty.last_request)
        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(self.mock_response._get_quota(),
                         actual_response.content)

    def test_update_quota(self):
        HTTPretty.register_uri(HTTPretty.PUT, self.quotas_uri,
                               body=self.mock_response._get_quota())
        actual_response = self.quotas_client.\
            update_quota(self.TENANT_ID, security_groups=45)

        expected_request_body = '{"quota_set": {"security_groups": 45}}'
        self._assert_default_headers_in_request(HTTPretty.last_request)
        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(HTTPretty.last_request.body,
                         expected_request_body)
        self.assertEqual(self.mock_response._get_quota(),
                         actual_response.content)

    def test_delete_quota(self):
        HTTPretty.register_uri(HTTPretty.DELETE, self.quotas_uri, status=202)
        actual_response = self.quotas_client.delete_quota(self.TENANT_ID)

        self.assertEqual(202, actual_response.status_code)


if __name__ == '__main__':
    unittest.main()
