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
import xml.etree.ElementTree as ET

from cloudcafe.compute.servers_api.models.requests import CreateServer


class CreateServerJSONDomainTest(object):

    def test_block_device_mapping_json(self):
        block = ('"block_device_mapping": [{"device_name": "vda", '
                 '"delete_on_termination": "0", '
                 '"volume_id": "sample_id"}]')
        self.assertIn(block, self.server_request_json,
                      msg="Block Mapping was not found in serialized request")


class CreateServerXMLDomainTest(object):

    def test_block_device_mapping_xml(self):
        file_path = self.server_request_xml_child[0]._children[0]
        self.assertEqual(file_path.attrib['device_name'], 'vda')
        self.assertEqual(file_path.attrib['delete_on_termination'], '0')
        self.assertEqual(file_path.attrib['volume_id'], 'sample_id')


class CreateServerObjectJSON(unittest.TestCase, CreateServerJSONDomainTest):

    @classmethod
    def setUpClass(cls):

        block = [{"volume_id": "sample_id",
                  "delete_on_termination": "0", "device_name": "vda"}]

        server_request_object = CreateServer(
            name='cctestserver',
            flavor_ref='2',
            image_ref='sample-image-ref',
            block_device_mapping=block)

        cls.server_request_json = server_request_object.serialize('json')


class CreateServerObjectXML(unittest.TestCase, CreateServerXMLDomainTest):
    @classmethod
    def setUpClass(cls):

        block = [{"volume_id": "sample_id",
                  "delete_on_termination": "0", "device_name": "vda"}]

        server_request_object = CreateServer(
            name='cctestserver',
            flavor_ref='2',
            image_ref='sample-image-ref',
            block_device_mapping=block)

        cls.server_request = server_request_object.serialize('xml')
        root = ET.fromstring(cls.server_request)
        cls.server_request_xml = root.attrib
        cls.server_request_xml_child = root.getchildren()
