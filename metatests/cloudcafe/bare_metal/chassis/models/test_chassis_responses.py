"""
Copyright 2014 Rackspace

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

from cloudcafe.bare_metal.chassis.models.responses import Chassis, ChassisList


class ChassisListModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.chassis_json_response = \
            """
            {
               "chassis":[
                  {
                     "description":"ironic test chassis",
                     "links":[
                        {
                           "href":"http://192.168.159.128:6385/v1/chassis/1",
                           "rel":"self"
                        },
                        {
                           "href":"http://192.168.159.128:6385/v1/chassis/1",
                           "rel":"bookmark"
                        }
                     ],
                     "uuid":"1"
                  }
               ]
            }
            """
        cls.chassis_list = ChassisList.deserialize(
            cls.chassis_json_response, 'json')

    def test_list_chassis(self):
        self.assertEqual(len(self.chassis_list), 1)

        chassis = self.chassis_list[0]
        self.assertEqual(chassis.uuid, "1")
        self.assertEqual(chassis.description, "ironic test chassis")

        self.assertEqual(len(chassis.links), 2)
        for link in chassis.links:
            self.assertIn(link.rel, ['self', 'bookmark'])
            self.assertEqual(
                link.href,
                'http://192.168.159.128:6385/v1/chassis/1')


class ChassisModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.chassis_json_response = \
            """
            {
               "description":"ironic test chassis",
               "links":[
                  {
                     "href":"http://192.168.159.128:6385/v1/chassis/1",
                     "rel":"self"
                  },
                  {
                     "href":"http://192.168.159.128:6385/v1/chassis/1",
                     "rel":"bookmark"
                  }
               ],
               "extra":{
                  "key1":"value1"
               },
               "created_at":"2014-04-01T01:53:45+00:00",
               "updated_at":"2014-04-02T01:53:45+00:00",
               "nodes":[
                  {
                     "href":"http://192.168.159.128:6385/v1/chassis/1/nodes",
                     "rel":"self"
                  },
                  {
                     "href":"http://192.168.159.128:6385/chassis/1/nodes",
                     "rel":"bookmark"
                  }
               ],
               "uuid":"1"
            }
            """

        cls.chassis = Chassis.deserialize(cls.chassis_json_response, 'json')

    def test_chassis_description(self):
        self.assertEqual(self.chassis.description, "ironic test chassis")

    def test_chassis_links(self):
        self.assertEqual(len(self.chassis.links), 2)

        for link in self.chassis.links:
            self.assertIn(link.rel, ['self', 'bookmark'])
            self.assertEqual(
                link.href, 'http://192.168.159.128:6385/v1/chassis/1')

    def test_chassis_extra_metadata(self):
        self.assertEqual(len(self.chassis.extra), 1)
        self.assertEqual(self.chassis.extra.get('key1'), 'value1')

    def test_chassis_created_at(self):
        self.assertEqual(self.chassis.created_at, '2014-04-01T01:53:45+00:00')

    def test_chassis_updated_at(self):
        self.assertEqual(self.chassis.updated_at, '2014-04-02T01:53:45+00:00')

    def test_chassis_nodes(self):
        self.assertEqual(len(self.chassis.nodes), 2)

        for node in self.chassis.nodes:
            self.assertIn(node.rel, ['self', 'bookmark'])

            if node.rel == 'bookmark':
                self.assertEqual(
                    node.href,
                    'http://192.168.159.128:6385/chassis/1/nodes')
            else:
                self.assertEqual(
                    node.href,
                    'http://192.168.159.128:6385/v1/chassis/1/nodes')

    def test_chassis_uuid(self):
        self.assertEqual(self.chassis.uuid, '1')
