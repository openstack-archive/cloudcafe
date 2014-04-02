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
import xml.etree.ElementTree as ET

from cloudcafe.compute.extensions.extensions_api.models.request import \
    CreateServerFromVolume as CreateServer


class CreateV2BlockServerJSONDomainTest(object):

    def test_block_device_mapping_json(self):
        block = ('"block_device_mapping_v2": [{"boot_index": "0", '
                 '"uuid": "sample-id", '
                 '"source_type": "image", '
                 '"volume_size": "10", '
                 '"destination_type": "volume", '
                 '"delete_on_termination": "0"}]')
        self.assertIn(block, self.server_request_json,
                      msg="Block Mapping was not found in serialized request")


class CreateServerXMLDomainTest(object):

    def test_block_device_mapping_xml(self):
        file_path = self.server_request_xml_child[0]._children[0]
        self.assertEqual(file_path.attrib['boot_index'], '0')
        self.assertEqual(file_path.attrib['uuid'], 'sample-id')
        self.assertEqual(file_path.attrib['source_type'], 'image')
        self.assertEqual(file_path.attrib['destination_type'], 'volume')
        self.assertEqual(file_path.attrib['delete_on_termination'], '0')
        self.assertEqual(file_path.attrib['volume_size'], '10')


class CreateServerObjectJSON(unittest.TestCase,
                             CreateV2BlockServerJSONDomainTest):
    @classmethod
    def setUpClass(cls):

        block = [{"boot_index": "0", "uuid": "sample-id",
                  "volume_size": "10", "source_type": "image",
                  "destination_type": "volume", "delete_on_termination": "0"}]

        server_request_object = CreateServer(
            name='cctestserver',
            flavor_ref='performance1-8',
            max_count='1',
            min_count='1',
            networks=[{"uuid": "sample-uuid"},
                      {"uuid": "sample-uuid"}],
            block_device_mapping_v2=block)

        cls.server_request_json = server_request_object.serialize('json')


class CreateServerObjectXML(unittest.TestCase, CreateServerXMLDomainTest):
    @classmethod
    def setUpClass(cls):

        block = [{"boot_index": "0", "uuid": "sample-id",
                  "volume_size": "10", "source_type": "image",
                  "destination_type": "volume", "delete_on_termination": "0"}]

        server_request_object = CreateServer(
            name='cctestserver',
            flavor_ref='performance1-8',
            max_count='1',
            min_count='1',
            networks=[{"uuid": "sample-uuid"},
                      {"uuid": "sample-uuid"}],
            block_device_mapping_v2=block)

        cls.server_request = server_request_object.serialize('xml')
        root = ET.fromstring(cls.server_request)
        cls.server_request_xml = root.attrib
        cls.server_request_xml_child = root.getchildren()
