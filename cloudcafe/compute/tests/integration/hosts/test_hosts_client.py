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

from cloudcafe.compute.hosts_api.client import HostsClient
from cloudcafe.compute.tests.integration.fixtures import IntegrationTestFixture
from cloudcafe.compute.tests.integration.hosts.responses\
    import HostsMockResponse


HOST_NAME = "787f4f6dda1b409bb8b2f9082349690e"


class HostsClientTest(IntegrationTestFixture):

    @classmethod
    def setUpClass(cls):
        super(HostsClientTest, cls).setUpClass()
        cls.hosts_client = HostsClient(
            url=cls.COMPUTE_API_ENDPOINT,
            auth_token=cls.AUTH_TOKEN,
            serialize_format=cls.FORMAT,
            deserialize_format=cls.FORMAT
        )
        cls.hosts_uri = "{0}/os-hosts".format(cls.COMPUTE_API_ENDPOINT)
        cls.host_uri = "{0}/{1}".format(cls.hosts_uri, HOST_NAME)
        cls.mock_response = HostsMockResponse(cls.FORMAT)

    def test_list_hosts(self):
        httpretty.register_uri(httpretty.GET, self.hosts_uri,
                               body=self.mock_response.list_hosts())
        response = self.hosts_client.list_hosts()
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.mock_response.list_hosts(),
                         response.content)

    def test_get_host(self):
        httpretty.register_uri(httpretty.GET, self.host_uri,
                               body=self.mock_response.get_host())
        response = self.hosts_client.get_host(HOST_NAME)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.mock_response.get_host(), response.content)


if __name__ == '__main__':
    unittest.main()
