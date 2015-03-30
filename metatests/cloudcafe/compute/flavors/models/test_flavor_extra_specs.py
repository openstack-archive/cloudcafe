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

from cloudcafe.compute.flavors_api.models.flavor_extra_specs \
    import FlavorExtraSpecs


class FlavorExtraSpecModelTest(object):

    def test_flavor_id(self):
        self.assertEqual(self.flavor_spec.get('field1'), '1')
        self.assertEqual(self.flavor_spec.get('field2'), '2')
        self.assertEqual(self.flavor_spec.get('field3'), '3')


class FlavorExtraSpecXMLTest(unittest.TestCase, FlavorExtraSpecModelTest):

    @classmethod
    def setUpClass(cls):
        cls.spec_xml = \
            """
            <extra_specs>
            <field1>1</field1>
            <field2>2</field2>
            <field3>3</field3>
            </extra_specs>
            """
        cls.flavor_spec = FlavorExtraSpecs.deserialize(cls.spec_xml, 'xml')


class FlavorExtraSpecJSONTest(unittest.TestCase, FlavorExtraSpecModelTest):

    @classmethod
    def setUpClass(cls):
        cls.spec_json = \
            """
            {"extra_specs": {"field1": "1", "field2": "2", "field3": "3"}}
            """
        cls.flavor_spec = FlavorExtraSpecs.deserialize(cls.spec_json, 'json')
