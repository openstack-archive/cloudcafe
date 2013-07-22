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

from cloudcafe.compute.extensions.vnc_console_api.models.vnc_console import VncConsoleOutput


class VncConsoleOutputDomainTest():

    def test_console_output_attributes(self):
        self.assertEqual(self.console_output.output, "some output")


class VncConsoleOutputDomainJSONTest(unittest.TestCase, VncConsoleOutputDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.console_output_json = """
        {"output": "some output"}
        """
        cls.console_output = VncConsoleOutput.deserialize(
            cls.console_output_json, "json")


class VncConsoleOutputDomainXMLTest(unittest.TestCase, VncConsoleOutputDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.console_output_xml = (
            """<?xml version='1.0' encoding='UTF-8'?>
               <output>some output</output>""")
        cls.console_output = VncConsoleOutput.deserialize(
            cls.console_output_xml, "xml")
