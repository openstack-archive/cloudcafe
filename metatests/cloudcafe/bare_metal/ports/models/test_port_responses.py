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

from cloudcafe.bare_metal.ports.models.responses import Port, Ports


class PortsModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ports_json = \
            """
            {
               "ports":[
                  {
                     "uuid":"1",
                     "links":[
                        {
                           "href":"http://192.168.159.128:6385/v1/ports/1",
                           "rel":"self"
                        },
                        {
                           "href":"http://192.168.159.128:6385/ports/1",
                           "rel":"bookmark"
                        }
                     ],
                     "address":"52:54:00:e5:57:d5"
                  },
                  {
                     "uuid":"2",
                     "links":[
                        {
                           "href":"http://192.168.159.128:6385/v1/ports/2",
                           "rel":"self"
                        },
                        {
                           "href":"http://192.168.159.128:6385/ports/2",
                           "rel":"bookmark"
                        }
                     ],
                     "address":"52:54:00:b1:dc:51"
                  },
                  {
                     "uuid":"3",
                     "links":[
                        {
                           "href":"http://192.168.159.128:6385/v1/ports/3",
                           "rel":"self"
                        },
                        {
                           "href":"http://192.168.159.128:6385/ports/3",
                           "rel":"bookmark"
                        }
                     ],
                     "address":"52:54:00:fe:cd:90"
                  }
               ]
            }
            """
        cls.ports = Ports.deserialize(cls.ports_json, 'json')

    def test_ports(self):
        self.assertEqual(len(self.ports), 3)

    def test_individual_port(self):
        self.assertTrue(
            any([port for port in self.ports if port.uuid == '1']))
        self.assertTrue(
            any([port for port in self.ports if port.uuid == '2']))
        self.assertTrue(
            any([port for port in self.ports if port.uuid == '3']))


class PortModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.port_json = \
            """
            {
               "node_uuid":"4353282d-7ae6-4b77-aec7-172555333bfa",
               "uuid":"1",
               "links":[
                  {
                     "href":"http://192.168.159.128:6385/v1/ports/1",
                     "rel":"self"
                  },
                  {
                     "href":"http://192.168.159.128:6385/ports/1",
                     "rel":"bookmark"
                  }
               ],
               "extra":{
                  "vif_port_id":"9ac29ee5-2fce-4cc0-8db1-2e4c3a3001c9"
               },
               "created_at":"2014-04-01T01:53:48+00:00",
               "updated_at":"2014-04-01T01:56:04+00:00",
               "address":"52:54:00:b1:dc:51"
            }
            """
        cls.port = Port.deserialize(cls.port_json, 'json')

    def test_port_node_uuid(self):
        self.assertEqual(
            self.port.node_uuid, "4353282d-7ae6-4b77-aec7-172555333bfa")

    def test_port_uuid(self):
        self.assertEqual(
            self.port.uuid, "1")

    def test_port_links(self):
        self.assertEqual(len(self.port.links), 2)

        for link in self.port.links:
            self.assertIn(link.rel, ['self', 'bookmark'])
            if link.rel == 'bookmark':
                self.assertEqual(
                    link.href,
                    'http://192.168.159.128:6385/ports/1')
            else:
                self.assertEqual(
                    link.href,
                    'http://192.168.159.128:6385/v1/ports/1')

    def test_port_extra_metadata(self):
        self.assertEqual(len(self.port.extra), 1)
        self.assertEqual(
            self.port.extra.get('vif_port_id'),
            '9ac29ee5-2fce-4cc0-8db1-2e4c3a3001c9')

    def test_port_created_at(self):
        self.assertEqual(self.port.created_at, '2014-04-01T01:53:48+00:00')

    def test_port_updated_at(self):
        self.assertEqual(self.port.updated_at, '2014-04-01T01:56:04+00:00')

    def test_port_address(self):
        self.assertEqual(self.port.address, '52:54:00:b1:dc:51')
