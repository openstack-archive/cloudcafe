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


class VncConsoleMockResponse():

    def __init__(self, format):
        self.format = format

    def get_console(self):
        return getattr(self, '_{0}_console'.format(self.format))()

    def get_console_output(self):
        return getattr(self, '_{0}_console_output'.format(self.format))()

    def _json_console(self):
        return """
        {
        "console":
            {
            "type": "novnc",
            "url": "http://example.com/vnc_auto.html?token=1234"
             }
        }"""

    def _xml_console(self):
        return """
        <?xml version='1.0' encoding='UTF-8'?>
        <console>
            <type>novnc</type>
            <url>http://example.com/vnc_auto.html?token=1234</url>
        </console>"""

    def _json_console_output(self):
        return """
        {
            "output": "FAKE CONSOLE OUTPUT\nANOTHER\nLAST LINE"
        }"""

    def _xml_console_output(self):
        return """
        <?xml version='1.0' encoding='UTF-8'?>
        <output>FAKE CONSOLE OUTPUT
        ANOTHER LAST LINE
        </output>"""
