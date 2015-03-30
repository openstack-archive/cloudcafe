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

from cloudcafe.compute.extensions.vnc_console_api.models.requests\
    import GetVncConsole


class ConsoleRequestsTest(unittest.TestCase):
    def test_serialize_get_console_request_to_json(self):
        request_obj = GetVncConsole(type="novnc")
        json_serialized_request = request_obj.serialize("json")
        expected_json = '{"os-getVNCConsole": {"type": "novnc"}}'
        self.assertEqual(json_serialized_request, expected_json)

    def test_serialize_get_console_request_to_xml(self):
        request_obj = GetVncConsole(type="novnc")
        xml_serialized_request = request_obj.serialize("xml")
        expected_xml = ('<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
                        '<os-getVNCConsole type="novnc" />')
        self.assertEqual(xml_serialized_request,
                         expected_xml.replace("\n", " "))
