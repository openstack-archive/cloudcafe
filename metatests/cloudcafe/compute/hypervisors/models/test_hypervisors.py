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
from cloudcafe.compute.hypervisors_api.model.hypervisors import Hypervisor


class HypervisorDomainTest():

    def test_hypervisor_attr(self):
        assert self.hypervisor[0].id == "1"
        assert self.hypervisor[0].hypervisor_hostname == "hypervisor_test"


class HypervisorDomainJSONTest(unittest.TestCase, HypervisorDomainTest):

    @classmethod
    def setUp(cls):
        cls.hypervisor_json = ('{"hypervisors": [{'
                               '"id": "1", '
                               '"hypervisor_hostname": "hypervisor_test"}]}')
        cls.hypervisor = Hypervisor.deserialize(cls.hypervisor_json, "json")


class HypervisorDomainXMLTest(unittest.TestCase, HypervisorDomainTest):

    @classmethod
    def setUp(cls):
        cls.hypervisor_xml = ('<?xml version="1.0" encoding="UTF-8"?>'
                              '<hypervisors><hypervisor id="1" '
                              'hypervisor_hostname="hypervisor_test"/>'
                              '</hypervisors>')
        cls.hypervisor = Hypervisor.deserialize(cls.hypervisor_xml, "xml")


class HypervisorServerCollectionDomainTest(object):

    def test_hypervisor_servers_length(self):
        assert len(self.hypervisor.servers) == 2

    def test_hypervisor_servers_attr(self):
        assert ("server_one" in
                [server.name for server in self.hypervisor.servers])
        assert ("server_two" in
                [server.name for server in self.hypervisor.servers])
        assert ("b1ea4f1b-201c-47c5-95b9-c6fe2df39af0" in
                [server.id for server in self.hypervisor.servers])
        assert ("9327b134-b1f5-43ec-a8f1-2b6eb153c739" in
                [server.id for server in self.hypervisor.servers])


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
        cls.hypervisor = Hypervisor.deserialize(cls.hypervisor_json, "json")


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
        cls.hypervisor = Hypervisor.deserialize(cls.hypervisor_xml,
                                                "xml")
