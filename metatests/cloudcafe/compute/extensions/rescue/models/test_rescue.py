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

from cloudcafe.compute.extensions.rescue_api.models.responses \
    import RescueResponse


class RescueResponseModelTest(object):

    def test_admin_password(self):
        self.assertEqual(self.rescue.admin_pass, 'MySecretPass')

class RescueResponseXMLModelTest(unittest.TestCase, RescueResponseModelTest):

    @classmethod
    def setUpClass(cls):
        cls.rescue_xml = '<adminPass>MySecretPass</adminPass>'
        cls.rescue = RescueResponse.deserialize(cls.rescue_xml, 'xml')


class RescueResponseJSONModelTest(unittest.TestCase, RescueResponseModelTest):

    @classmethod
    def setUpClass(cls):
        cls.rescue_json = '{"adminPass": "MySecretPass"}'
        cls.rescue = RescueResponse.deserialize(cls.rescue_json, 'json')
