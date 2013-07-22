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

from cafe.engine.clients.rest import AutoMarshallingRestClient

from cloudcafe.compute.extensions.vnc_console_output_api.models.requests\
    import GetConsoleOutput

from cloudcafe.compute.extensions.vnc_console_output_api.models.\
    vnc_console_output import VncConsoleOutput


class VncConsoleOutputClient(AutoMarshallingRestClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(VncConsoleOutputClient, self).__init__(
            serialize_format, deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def get_vnc_console_output(self, server_id, length,
                               requestslib_kwargs=None):
        """
        @summary: Returns Console Output for a server
        @param server_id: The id of an existing server
        @type server_id: String
        @param length: Number of lines of console output
        @type length: String
        @return: Console Output for the server
        @rtype: Requests.response
        """
        url = '{base_url}/servers/{server_id}/action'.format(
            base_url=self.url, server_id=server_id)
        get_console_output_request_object = GetConsoleOutput(length=length)
        resp = self.request('POST', url,
                            request_entity=get_console_output_request_object,
                            response_entity_type=VncConsoleOutput,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
