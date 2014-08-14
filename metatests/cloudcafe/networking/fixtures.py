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


class ClientTestFixture(unittest.TestCase):

    AUTH_TOKEN = '2a48b789fe214791915f0d7cd8b669eb'
    NETWORKING_API_ENDPOINT = 'http://localhost:9696/v2.0'
    TENANT_ID = '831861'
    FORMAT = 'json'
    CONTENT_TYPE = 'application/{0}'.format(FORMAT)
    ACCEPT = 'application/{0}'.format(FORMAT)

    @classmethod
    def setUp(cls):
        HTTPretty.reset()
        HTTPretty.enable()

    @classmethod
    def tearDown(cls):
        HTTPretty.disable()

    def _assert_default_headers_in_request(self, request):
        assert request.headers['X-Auth-Token'] == self.AUTH_TOKEN
        assert request.headers['Content-Type'] == self.CONTENT_TYPE
        assert request.headers['Accept'] == self.ACCEPT
