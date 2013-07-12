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
from cloudcafe.compute.hypervisors_api.model.hypervisor import HypervisorMin


class HypervisorMinDomainTest(object):

    def test_hypervisor_attr(self):
        self.assertEqual(self.hypervisor[0].id, "1")
        self.assertEqual(self.hypervisor[0].hypervisor_hostname,
                         "hypervisor_test")


class HypervisorMinDomainJSONTest(unittest.TestCase, HypervisorMinDomainTest):

    @classmethod
    def setUp(cls):
        cls.hypervisor_json = ('{"hypervisors": [{'
                               '"id": "1", '
                               '"hypervisor_hostname": "hypervisor_test"}]}')
        cls.hypervisor = HypervisorMin.deserialize(cls.hypervisor_json, "json")


class HypervisorMinDomainXMLTest(unittest.TestCase, HypervisorMinDomainTest):

    @classmethod
    def setUp(cls):
        cls.hypervisor_xml = ('<?xml version="1.0" encoding="UTF-8"?>'
                              '<hypervisors><hypervisor id="1" '
                              'hypervisor_hostname="hypervisor_test"/>'
                              '</hypervisors>')
        cls.hypervisor = HypervisorMin.deserialize(cls.hypervisor_xml, "xml")


class HypervisorServerCollectionDomainTest(object):

    def test_hypervisor_servers_length(self):
        self.assertEqual(len(self.hypervisors[0].servers), 2)

    def test_hypervisor_servers_attr(self):
        self.assertIn("server_one", [server.name for server in
                                     self.hypervisors[0].servers])
        self.assertIn("server_two", [server.name for server in
                                     self.hypervisors[0].servers])
        self.assertIn("b1ea4f1b-201c-47c5-95b9-c6fe2df39af0",
                      [server.id for server in self.hypervisors[0].servers])
        self.assertIn("9327b134-b1f5-43ec-a8f1-2b6eb153c739",
                      [server.id for server in self.hypervisors[0].servers])


class ServersDomainCollectionJSONTest(unittest.TestCase,
                                      HypervisorServerCollectionDomainTest):

    @classmethod
    def setUp(cls):
        cls.hypervisor_json = ('{"hypervisors": [{'
                               '"id": 1, '
                               '"hypervisor_hostname": "hypervisor_test", '
                               '"servers": [{'
                               '"uuid": '
                               '"b1ea4f1b-201c-47c5-95b9-c6fe2df39af0", '
                               '"name": "server_one"}, '
                               '{"uuid": '
                               '"9327b134-b1f5-43ec-a8f1-2b6eb153c739", '
                               '"name": "server_two"}]}]}')
        cls.hypervisors = HypervisorMin.deserialize(cls.hypervisor_json,
                                                    "json")


class ServersDomainCollectionXMLTest(unittest.TestCase,
                                     HypervisorServerCollectionDomainTest):

    @classmethod
    def setUp(cls):
        cls.hypervisor_xml = ('<?xml version="1.0" encoding="UTF-8"?>'
                              '<hypervisors>'
                              '<hypervisor '
                              'id="1" '
                              'hypervisor_hostname="hypervisor_test">'
                              '<servers>'
                              '<server name="server_one" '
                              'uuid="b1ea4f1b-201c-47c5-95b9-c6fe2df39af0"/>'
                              '<server name="server_two" '
                              'uuid="9327b134-b1f5-43ec-a8f1-2b6eb153c739"/>'
                              '</servers></hypervisor></hypervisors>')
        cls.hypervisors = HypervisorMin.deserialize(cls.hypervisor_xml,
                                                    "xml")
