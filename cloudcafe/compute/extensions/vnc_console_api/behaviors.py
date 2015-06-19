"""
Copyright 2015 Rackspace

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

import telnetlib

from cloudcafe.compute.common.behaviors import BaseComputeBehavior


class VncConsoleBehaviors(BaseComputeBehavior):

    def get_vnc_console_response(self, url):
        """
        @summary:Returns vnc console url status response
        @return: Response Object containing vnc console url response
        @rtype: Request Response Object
        """
        HOST = url.split('/')[2].split(':')[0]
        PORT = url.split('/')[2].split(':')[1]
        TOKEN = url.split('/')[3]

        telnet_session = telnetlib.Telnet(str(HOST), str(PORT))

        telnet_session.write("GET {0} HTTP/1.1\r\n".format(TOKEN))
        telnet_session.write("ls\n")
        telnet_session.write("exit\n")

        response = telnet_session.read_until("OK".encode())

        return response
