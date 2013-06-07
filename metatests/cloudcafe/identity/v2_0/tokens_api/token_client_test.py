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

from unittest import TestCase
from cloudcafe.identity.v2_0.tokens_api.client import TokenAPI_Client
from httpretty import HTTPretty

IDENTITY_ENDPOINT_URL = "http://localhost:9292"


class TokenClientTest(TestCase):
    def setUp(self):
        self.token_api_client = TokenAPI_Client(
            url=IDENTITY_ENDPOINT_URL,
            auth_token="AUTH_TOKEN",
            serialize_format="json",
            deserialize_format="json",
        )

        HTTPretty.enable()

    def test_authenticate(self):
        url = "{0}/v2.0/tokens".format(IDENTITY_ENDPOINT_URL)
        HTTPretty.register_uri(HTTPretty.POST, url,
                               body=self._build_authentication_response(),
                               content_type="application/json")

        actual_response = self.token_api_client.authenticate()

        assert HTTPretty.last_request.headers['X-Auth-Token'] == 'AUTH_TOKEN'
        assert HTTPretty.last_request.headers['Content-Type'] == \
            'application/json'
        assert HTTPretty.last_request.headers['Accept'] == 'application/json'
        assert actual_response.status_code == 200
        assert self._build_authentication_response() == actual_response.content

    def _build_authentication_response(self):
        return "MOCK_RESPONSE_CONTENT"
