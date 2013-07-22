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
from cloudcafe.compute.servers_api.client import ServersClient

from metatests.cloudcafe.compute.servers.client.responses\
    import ConsoleMockResponse
from metatests.cloudcafe.compute.fixtures import ClientTestFixture


class ServersClientTest(ClientTestFixture):

    @classmethod
    def setUpClass(cls):
        super(ServersClientTest, cls).setUpClass()
        cls.servers_client = ServersClient(
            url=cls.COMPUTE_API_ENDPOINT,
            auth_token=cls.AUTH_TOKEN,
            serialize_format=cls.FORMAT,
            deserialize_format=cls.FORMAT
        )
        cls.console_uri = "{0}/servers/{1}/action".format(
            cls.COMPUTE_API_ENDPOINT, cls.SERVER_ID)
        cls.mock_response = ConsoleMockResponse(cls.FORMAT)

    def test_get_console(self):
        HTTPretty.register_uri(HTTPretty.POST, self.console_uri,
                               body=self.mock_response.get_console())
        response = self.servers_client.get_console(
            server_id=self.SERVER_ID, type="novnc")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.mock_response.get_console(), response.content)

    def test_get_console_output(self):
        HTTPretty.register_uri(HTTPretty.POST, self.console_uri,
                               body=self.mock_response.get_console_output())
        response = self.servers_client.get_console_output(
            server_id=self.SERVER_ID, length=50)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.mock_response.get_console_output(),
                         response.content)
