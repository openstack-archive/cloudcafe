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

from cloudcafe.compute.common.constants import Constants
from cloudcafe.compute.flavors_api.models.flavor import Flavor


class FlavorModelTest(object):

    def test_flavor_id(self):
        self.assertEqual(self.flavor.id, "2")

    def test_flavor_name(self):
        self.assertEqual(self.flavor.name, "512MB Standard Instance")

    def test_flavor_vcpus(self):
        self.assertEqual(self.flavor.vcpus, 1)

    def test_flavor_ram(self):
        self.assertEqual(self.flavor.ram, 512)

    def test_flavor_disk(self):
        self.assertEqual(self.flavor.disk, 20)

    def test_flavor_swap(self):
        self.assertEqual(self.flavor.swap, 512)

    def test_flavor_rxtx_factor(self):
        self.assertEqual(self.flavor.rxtx_factor, 2.0)

    def test_flavor_ephemeral_disk(self):
        self.assertEqual(self.flavor.ephemeral_disk, 250)

    def test_flavor_links_self(self):
        self.assertEqual(
            self.flavor.links.self,
            "https://127.0.0.1/v2/660/flavors/2")

    def test_flavor_links_bookmark(self):
        self.assertEqual(
            self.flavor.links.bookmark,
            "https://127.0.0.1/660/flavors/2")

    def test_flavor_extra_specs(self):
        self.assertEqual(self.flavor.extra_specs.get('field1'), '1')


class FlavorXMLModelTest(unittest.TestCase, FlavorModelTest):

    @classmethod
    def setUpClass(cls):
        cls.flavor_xml = \
            """
            <flavor xmlns:atom="http://www.w3.org/2005/Atom"
            xmlns:OS-FLV-EXT-DATA="{extra_data}"
            xmlns:OS-FLV-WITH-EXT-SPECS="{extra_specs}"
            xmlns="http://docs.openstack.org/compute/api/v1.1"
            disk="20" vcpus="1" ram="512" name="512MB Standard Instance"
            id="2" swap="512" rxtx_factor="2.0"
            OS-FLV-EXT-DATA:ephemeral="250">
            <OS-FLV-WITH-EXT-SPECS:extra_specs>
            <field1>1</field1>
            </OS-FLV-WITH-EXT-SPECS:extra_specs>
            <atom:link href="https://127.0.0.1/v2/660/flavors/2" rel="self"/>
            <atom:link href="https://127.0.0.1/660/flavors/2" rel="bookmark"/>
            </flavor>
            """.format(extra_specs=Constants.XML_FLAVOR_EXTRA_SPECS,
                       extra_data=Constants.XML_FLAVOR_EXTRA_DATA)
        cls.flavor = Flavor.deserialize(cls.flavor_xml, 'xml')


class FlavorJSONModelTest(unittest.TestCase, FlavorModelTest):

    @classmethod
    def setUpClass(cls):
        cls.flavor_json = \
            """
            {
              "flavor" : {
                "name" : "512MB Standard Instance",
                "links" : [
                  {
                    "href" : "https://127.0.0.1/v2/660/flavors/2",
                    "rel" : "self"
                  },
                  {
                    "href" : "https://127.0.0.1/660/flavors/2",
                    "rel" : "bookmark"
                  }
                ],
                "ram" : 512,
                "vcpus" : 1,
                "swap" : 512,
                "rxtx_factor" : 2.0,
                "disk" : 20,
                "id" : "2",
                "OS-FLV-EXT-DATA:ephemeral" : 250,
                "OS-FLV-WITH-EXT-SPECS:extra_specs": {"field1": "1"}
              }
            }
            """
        cls.flavor = Flavor.deserialize(cls.flavor_json, 'json')
