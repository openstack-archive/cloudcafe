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

import unittest

from cloudcafe.compute.extensions.floating_ips_api.models.requests import \
    CreateFloatingIP


class ConsoleRequestsTest(unittest.TestCase):

    def test_serialize_json_create_floating_ip_request(self):
        request_obj = CreateFloatingIP(pool='public')
        json_serialized_request = request_obj.serialize("json")
        expected_json = '{"pool": "public"}'
        self.assertEqual(json_serialized_request, expected_json)