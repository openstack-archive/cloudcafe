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

from cloudcafe.compute.hypervisors_api.client import HypervisorsClient
from metatests.cloudcafe.compute.fixtures import ClientTestFixture
from metatests.cloudcafe.compute.hypervisors.client.responses \
    import HypervisorsClientMockResponse

HYPERVISOR_HOSTNAME = "hypervisor_test"


class HypervisorsClientTest(ClientTestFixture):

    @classmethod
    def setUpClass(cls):
        super(HypervisorsClientTest, cls).setUpClass()
        cls.hypervisor_client = HypervisorsClient(
            url=cls.COMPUTE_API_ENDPOINT,
            auth_token=cls.AUTH_TOKEN,
            serialize_format=cls.FORMAT,
            deserialize_format=cls.FORMAT)
        cls.hypervisors_uri = ("{0}/os-hypervisors".
                               format(cls.COMPUTE_API_ENDPOINT))
        cls.hypervisors_in_detail_uri = ("{0}/os-hypervisors/detail".
                                         format(cls.COMPUTE_API_ENDPOINT))
        cls.hypervisor_servers_uri = ("{0}/{1}/servers".
                                      format(cls.hypervisors_uri,
                                      HYPERVISOR_HOSTNAME))
        cls.mock_response = HypervisorsClientMockResponse()

    def test_list_hypervisors(self):
        HTTPretty.register_uri(HTTPretty.GET, self.hypervisors_uri,
                               body=self.mock_response.
                               list_hypervisors())
        response = self.hypervisor_client.list_hypervisors()
        self.assertEqual(200, response.status_code)
        self._assert_default_headers_in_request(HTTPretty.last_request)
        self.assertEqual(HypervisorsClientMockResponse.list_hypervisors(),
                         response.content)

    def test_list_hypervisors_in_detail(self):
        HTTPretty.register_uri(HTTPretty.GET, self.hypervisors_in_detail_uri,
                               body=self.mock_response.
                               list_hypervisors_in_detail())
        response = self.hypervisor_client.list_hypervisors_with_detail()
        self.assertEqual(200, response.status_code)
        self._assert_default_headers_in_request(HTTPretty.last_request)
        self.assertEqual(
            response.content,
            HypervisorsClientMockResponse.list_hypervisors_in_detail())

    def test_list_hypervisor_servers(self):
        HTTPretty.register_uri(HTTPretty.GET, self.hypervisor_servers_uri,
                               body=self.mock_response.
                               list_hypervisor_servers())
        response = self.hypervisor_client.\
            list_hypervisor_servers(HYPERVISOR_HOSTNAME)
        self.assertEqual(200, response.status_code)
        self._assert_default_headers_in_request(HTTPretty.last_request)
        self.assertEqual(
            HypervisorsClientMockResponse.list_hypervisor_servers(),
            response.content)
