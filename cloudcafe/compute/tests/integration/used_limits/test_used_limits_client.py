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
import httpretty

from cloudcafe.compute.tests.integration.fixtures import IntegrationTestFixture
from cloudcafe.compute.tests.integration.used_limits.responses \
    import UsedLimitsMockResponse
from cloudcafe.compute.extensions.used_limits.client import UsedLimitsClient


USER_TENANTID = "c34dbd5940514344b54747487266a4b6"


class UsedLimitForAdminClientTest(IntegrationTestFixture):

    @classmethod
    def setUpClass(cls):
        super(UsedLimitForAdminClientTest, cls).setUpClass()
        cls.used_limit_client = UsedLimitsClient(
            url=cls.COMPUTE_API_ENDPOINT,
            auth_token=cls.AUTH_TOKEN,
            serialize_format=cls.FORMAT,
            deserialize_format=cls.FORMAT)
        cls.used_limit_uri = "{0}/limits?tenant_id={1}".\
            format(cls.COMPUTE_API_ENDPOINT, USER_TENANTID)
        cls.mock_response = UsedLimitsMockResponse()

    @httpretty.activate
    def test_get_used_limits(self):
        httpretty.register_uri(httpretty.GET, self.used_limit_uri,
                               body=self.mock_response.get_used_limit())
        response = self.used_limit_client.\
            get_used_limits_for_user(USER_TENANTID)
        self.assertEqual(200, response.status_code)
        self.assertEqual(UsedLimitsMockResponse.get_used_limit(),
                         response.content)


if __name__ == '__main__':
    unittest.main()
