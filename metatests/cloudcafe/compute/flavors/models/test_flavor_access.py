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

from cloudcafe.compute.flavors_api.models.flavor_access \
    import FlavorAccess, FlavorAccessList


class FlavorAccessModelTest(object):

    def test_flavor_access_entries(self):
        first_entry = FlavorAccess(flavor_id='42', tenant_id='user1')
        second_entry = FlavorAccess(flavor_id='84', tenant_id='user2')

        self.assertIn(first_entry, self.access_list)
        self.assertIn(second_entry, self.access_list)


class FlavorAccessXMLTest(unittest.TestCase, FlavorAccessModelTest):

    @classmethod
    def setUpClass(cls):
        cls.access_xml = \
            """
            <flavor_access>
            <access tenant_id="user1" flavor_id="42"/>
            <access tenant_id="user2" flavor_id="84"/>
            </flavor_access>
            """
        cls.access_list = FlavorAccessList.deserialize(cls.access_xml, 'xml')


class FlavorAccessJSONTest(unittest.TestCase, FlavorAccessModelTest):

    @classmethod
    def setUpClass(cls):
        cls.access_json = \
            """
            {
                "flavor_access": [
                    {
                        "flavor_id": "42",
                        "tenant_id": "user1"
                    },
                    {
                        "flavor_id": "84",
                        "tenant_id": "user2"
                    }
                ]
            }
            """
        cls.access_list = FlavorAccessList.deserialize(cls.access_json, 'json')
