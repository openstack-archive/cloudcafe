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

from cloudcafe.compute.extensions.vnc_console_api.models.vnc_console\
    import VncConsole


class VncConsoleDomainTest():

    def test_console_attributes(self):
        self.assertEqual(self.console.type, "novnc")
        self.assertEqual(self.console.url,
                         "http://example.com/vnc_auto.html?token=1234")


class VncConsoleDomainJSONTest(unittest.TestCase, VncConsoleDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.console_json = """
        {
        "console":
            {
            "type": "novnc",
            "url": "http://example.com/vnc_auto.html?token=1234"
             }
        }"""

        cls.console = VncConsole.deserialize(cls.console_json, "json")


class VncConsoleDomainXMLTest(unittest.TestCase, VncConsoleDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.console_xml = (
            """<?xml version='1.0' encoding='UTF-8'?>
               <console>
                <type>novnc</type>
                <url>http://example.com/vnc_auto.html?token=1234</url>
               </console>""")
        cls.console = VncConsole.deserialize(cls.console_xml, "xml")
