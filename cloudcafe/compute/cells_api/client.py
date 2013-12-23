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
from cloudcafe.compute.cells_api.model.cells import Cell


class CellsClient(AutoMarshallingHTTPClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        """
        @param url: Base URL for the compute service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """
        super(CellsClient, self).__init__(serialize_format,
                                          deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def get_cell_capacity_by_name(self, cell_name, requestslib_kwargs=None):
        """
        @summary: Returns a cell with capacities
        @return: Response
        @rtype: response
        """
        url = "{url}/os-cells/{cell_name}/show_capacities".\
            format(url=self.url, cell_name=cell_name)
        cell_response = self.request('GET', url,
                                     response_entity_type=Cell,
                                     requestslib_kwargs=requestslib_kwargs)
        return cell_response

    def get_aggregated_cell_capacity(self, requestslib_kwargs=None):
        """
        @summary: Returns aggregate cell capacity
        @return: Response
        @rtype: Response
        """
        url = "{url}/os-cells/show_capacities".format(url=self.url)
        cell_response = self.request('GET', url,
                                     response_entity_type=Cell,
                                     requestslib_kwargs=requestslib_kwargs)
        return cell_response
