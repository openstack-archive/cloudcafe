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

from cafe.engine.http.client import AutoMarshallingHTTPClient
from cloudcafe.compute.extensions.vnc_console_api.models.requests\
    import GetVncConsole
from cloudcafe.compute.extensions.vnc_console_api.models.vnc_console\
    import VncConsole


class VncConsoleClient(AutoMarshallingHTTPClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(VncConsoleClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def get_vnc_console(self, server_id, vnc_type,
                        requestslib_kwargs=None):
        """
        @summary: Returns Console for a server
        @param server_id: The id of an existing server
        @type server_id: String
        @param vnc_type: Type of console, i.e, novnc, xvnc
        @type vnc_type: String
        @return: A console for the server
        @rtype: Requests.response
        """
        request = GetVncConsole(type=vnc_type)

        url = '{base_url}/servers/{server_id}/action'.format(
            base_url=self.url, server_id=server_id)
        resp = self.request('POST', url,
                            response_entity_type=VncConsole,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
