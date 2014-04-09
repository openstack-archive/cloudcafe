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

from cloudcafe.bare_metal.chassis.models.responses import Chassis, ChassisList
from cloudcafe.bare_metal.chassis.models.requests import CreateChassis
from cloudcafe.bare_metal.nodes.models.responses import Nodes


class ChassisClient(AutoMarshallingHTTPClient):

    def __init__(
            self, url, auth_token, serialize_format=None,
            deserialize_format=None):

        super(ChassisClient, self).__init__(
            serialize_format, deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)

    def list_chassis(self, requestslib_kwargs=None):
        """
        @summary: Lists all chassis.
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/chassis'.format(base_url=self.url)
        resp = self.get(url, response_entity_type=ChassisList,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_chassis_with_details(self, requestslib_kwargs=None):
        """
        @summary: Lists all chassis with details.
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/chassis/detail'.format(base_url=self.url)
        resp = self.get(url, response_entity_type=ChassisList,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_nodes_for_chassis(self, uuid, requestslib_kwargs=None):
        """
        @summary: Lists all nodes associated with a chassis.
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/chassis/{chassis}/nodes'.format(
            base_url=self.url, chassis=uuid)
        resp = self.get(url, response_entity_type=Nodes,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_chassis(self, uuid, requestslib_kwargs=None):
        """
        @summary: Retrieves the details of an individual chassis.
        @param uuid: The uuid of an existing chassis
        @type uuid: String
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/chassis/{uuid}'.format(
            base_url=self.url, uuid=uuid)
        resp = self.get(url, response_entity_type=Chassis,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def create_chassis(self, description=None, extra=None,
                       requestslib_kwargs=None):
        """
        @summary: Creates a chassis from the provided parameters.
        @param description: Description of the chassis
        @type description: String
        @param description: Extra metadata for the chassis
        @type description: Dict
        @return: resp
        @rtype: Requests.response
        """
        request = CreateChassis(
            description=description, extra=extra)

        url = '{base_url}/chassis'.format(base_url=self.url)
        resp = self.post(url,
                         response_entity_type=Chassis,
                         request_entity=request,
                         requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_chassis(self, uuid, requestslib_kwargs=None):
        """
        @summary: Deletes the specified chassis.
        @param uuid: The uuid of a chassis
        @type uuid: String
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/chassis/{uuid}'.format(
            base_url=self.url, uuid=uuid)
        resp = self.delete(url, requestslib_kwargs=requestslib_kwargs)
        return resp
