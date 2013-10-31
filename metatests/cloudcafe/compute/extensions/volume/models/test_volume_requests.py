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
from cloudcafe.compute.extensions.volumes_api.models.requests import CreateVolume


class VolumeRequestsTest(unittest.TestCase):
    def test_serialize_get_console_request_to_json(self):
        request_obj = CreateVolume(display_name="vol-001",
                                   display_description="Another volume.",
                                   size=30,
                                   volume_type="289da7f8-6440-407c-9fb4-7db01ec49164",
                                   metadata={"contents": "junk"},
                                   availability_zone="us-east1")
        json_serialized_request = request_obj.serialize("json")
        expected_json = ('{"volume": {"display_name": "vol-001", "availability_zone": "us-east1",'
                         ' "volume_type":' ' "289da7f8-6440-407c-9fb4-7db01ec49164",'
                         ' "display_description": "Another volume.", "size": 30,'
                         ' "metadata": {"contents": "junk"}}}')
        self.assertEqual(json_serialized_request, expected_json)

    def test_serialize_get_console_request_to_xml(self):
        request_obj = CreateVolume(display_name="vol-001",
                                   display_description="Another volume.",
                                   size=30,
                                   volume_type="289da7f8-6440-407c-9fb4-7db01ec49164",
                                   metadata={"contents": "junk"},
                                   availability_zone="us-east1")
        xml_serialized_request = request_obj.serialize("xml")
        expected_xml = ('<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
                        '<volume availability_zone="us-east1"'
                        ' display_description="Another volume."'
                        ' display_name="vol-001" size="30"'
                        ' volume_type="289da7f8-6440-407c-9fb4-7db01ec49164">'
                        '<metadata>'
                        '<meta key="contents">junk</meta>'
                        '</metadata></volume>')
        self.assertEqual(xml_serialized_request, expected_xml)

