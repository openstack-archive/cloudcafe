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

from cloudcafe.compute.hypervisors_api.client import HypervisorsClient
from cloudcafe.compute.tests.integration.fixtures \
    import IntegrationTestFixture
from cloudcafe.compute.tests.integration.hypervisors.responses \
    import HypervisorsClientMockResponse

HYPERVISOR_HOSTNAME = "hypervisor_test"


class HypervisorsClientTest(IntegrationTestFixture):
    @classmethod
    def setUpClass(cls):
        super(HypervisorsClientTest, cls).setUpClass()
        cls.hypervisor_client = HypervisorsClient(
            url=cls.COMPUTE_API_ENDPOINT,
            auth_token=cls.AUTH_TOKEN,
            serialize_format=cls.FORMAT,
            deserialize_format=cls.FORMAT)
        cls.hypervisors_uri = "{0}/os-hypervisors". \
            format(cls.COMPUTE_API_ENDPOINT)
        cls.hypervisor_servers_uri = "{0}/{1}/servers". \
            format(cls.hypervisors_uri,
                   HYPERVISOR_HOSTNAME)
        cls.mock_response = HypervisorsClientMockResponse()

    @httpretty.activate
    def test_list_hypervisors(self):
        httpretty.register_uri(httpretty.GET, self.hypervisors_uri,
                               body=self.mock_response.
                               list_hypervisors())
        response = self.hypervisor_client.list_hypervisors()
        self.assertEqual(200, response.status_code)
        self._assert_default_headers_in_request(
            httpretty.HTTPretty.last_request)
        self.assertEqual(HypervisorsClientMockResponse.list_hypervisors(),
                         response.content)

    @httpretty.activate
    def test_list_hypervisor_servers(self):
        httpretty.register_uri(httpretty.GET, self.hypervisor_servers_uri,
                               body=self.mock_response.
                               list_hypervisor_servers())
        response = self.hypervisor_client. \
            list_hypervisor_servers(HYPERVISOR_HOSTNAME)
        self.assertEqual(200, response.status_code)
        self._assert_default_headers_in_request(
            httpretty.HTTPretty.last_request)
        self.assertEqual(HypervisorsClientMockResponse.
                         list_hypervisor_servers(),
                         response.content)


if __name__ == '__main__':
    unittest.main()