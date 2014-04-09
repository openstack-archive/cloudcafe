"""
Copyright 2014 Rackspace

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

from cloudcafe.bare_metal.drivers.models.responses import Driver, Drivers


class DriversClient(AutoMarshallingHTTPClient):

    def __init__(
            self, url, auth_token, serialize_format=None,
            deserialize_format=None):

        super(DriversClient, self).__init__(
            serialize_format, deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)

    def list_drivers(self, requestslib_kwargs=None):
        """
        @summary: Lists all drivers with details.
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/drivers'.format(base_url=self.url)
        resp = self.get(url, response_entity_type=Drivers,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_driver(self, name, requestslib_kwargs=None):
        """
        @summary: Retrieves the details of an individual driver.
        @param name: The uuid of an existing port
        @type name: String
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/drivers/{uuid}'.format(
            base_url=self.url, uuid=name)
        resp = self.get(url, response_entity_type=Driver,
                        requestslib_kwargs=requestslib_kwargs)
        return resp
