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

import json
import unittest

from cloudcafe.compute.common.models.metadata import Metadata, MetadataItem


class MetadataModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.metadata = Metadata()
        cls.metadata['key1'] = 'value1'

        cls.expected_xml = \
            ('<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
             '<metadata xmlns="http://docs.openstack.org/compute/api/v1.1">'
             '<meta key="key1">value1</meta>'
             '</metadata>')
        cls.expected_json = json.dumps({'metadata': {'key1': 'value1'}})

    def test_metadata_xml_serialization(self):
        serialized_metadata = self.metadata.serialize('xml')
        self.assertEqual(serialized_metadata, self.expected_xml)

    def test_metadata_xml_deserialization(self):
        metadata = Metadata.deserialize(self.expected_xml, 'xml')
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata.get('key1'), 'value1')

    def test_metadata_json_serialization(self):
        serialized_metadata = self.metadata.serialize('json')
        self.assertEqual(serialized_metadata, self.expected_json)

    def test_metadata_json_deserialization(self):
        metadata = Metadata.deserialize(self.expected_json, 'json')
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata.get('key1'), 'value1')


class MetadataItemModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.meta_item = MetadataItem()
        cls.meta_item['key1'] = 'value1'

        cls.expected_xml = \
            ('<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
             '<meta key="key1">value1</meta>')
        cls.expected_json = json.dumps({'meta': {'key1': 'value1'}})

    def test_metadata_item_json_serialization(self):
        serialized_metadata = self.meta_item.serialize('json')
        self.assertEqual(serialized_metadata, self.expected_json)

    def test_metadata_xml_serialization(self):
        serialized_metadata = self.meta_item.serialize('xml')
        self.assertEqual(serialized_metadata, self.expected_xml)

    def test_metadata_xml_deserialization(self):
        meta = MetadataItem.deserialize(self.expected_xml, 'xml')
        self.assertIsNotNone(meta)
        self.assertEqual(meta.get('key1'), 'value1')

    def test_metadata_json_deserialization(self):
        meta = MetadataItem.deserialize(self.expected_json, 'json')
        self.assertIsNotNone(meta)
        self.assertEqual(meta.get('key1'), 'value1')
