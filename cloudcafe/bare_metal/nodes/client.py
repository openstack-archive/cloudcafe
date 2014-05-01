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

from cloudcafe.bare_metal.common.models.patch import Patches
from cloudcafe.bare_metal.nodes.models.responses import (
    Node, Nodes, DriverInterfaces)
from cloudcafe.bare_metal.nodes.models.requests import (
    CreateNode, SetNodePowerState, SetNodeConsoleMode)
from cloudcafe.bare_metal.ports.models.responses import Ports


class NodesClient(AutoMarshallingHTTPClient):

    def __init__(
            self, url, auth_token, serialize_format=None,
            deserialize_format=None):

        super(NodesClient, self).__init__(
            serialize_format, deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)

    def list_nodes(self, requestslib_kwargs=None):
        """
        @summary: Lists all nodes.
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/nodes'.format(base_url=self.url)
        resp = self.get(url, response_entity_type=Nodes,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_nodes_with_details(self, requestslib_kwargs=None):
        """
        @summary: Lists all nodes with details.
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/nodes/detail'.format(base_url=self.url)
        resp = self.get(url, response_entity_type=Nodes,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_ports_for_node(self, uuid, requestslib_kwargs=None):
        """
        @summary: Lists all nodes with details.
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/nodes/{uuid}/ports'.format(
            base_url=self.url, uuid=uuid)
        resp = self.get(url, response_entity_type=Ports,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_node(self, uuid, requestslib_kwargs=None):
        """
        @summary: Retrieves the details of an individual node.
        @param uuid: The uuid of an existing node
        @type uuid: String
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/nodes/{uuid}'.format(
            base_url=self.url, uuid=uuid)
        resp = self.get(url, response_entity_type=Node,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def create_node(
            self, chassis_uuid, driver=None, properties=None,
            driver_info=None, extra=None, requestslib_kwargs=None):
        """
        @summary: Creates a node from the provided parameters.
        @param chassis_uuid: The chassis the node is associated with
        @type chassis_uuid: String
        @param driver: The driver used to control the node
        @type driver: String
        @param properties: The physical characteristics of the node
        @type properties: Dict
        @param driver_info: Configuration parameters for the driver
        @type driver_info: Dict
        @param extra: Extra metadata for the node
        @type extra: Dict
        @return: resp
        @rtype: Requests.response
        """
        request = CreateNode(
            chassis_uuid=chassis_uuid, driver=driver, properties=properties,
            driver_info=driver_info, extra=extra)

        url = '{base_url}/nodes'.format(base_url=self.url)
        resp = self.post(url,
                         response_entity_type=Node,
                         request_entity=request,
                         requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_node(self, uuid, requestslib_kwargs=None):
        """
        @summary: Deletes the specified node.
        @param uuid: The uuid of a node
        @type uuid: String
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/nodes/{uuid}'.format(
            base_url=self.url, uuid=uuid)
        resp = self.delete(url, requestslib_kwargs=requestslib_kwargs)
        return resp

    def set_node_power_state(self, uuid, state, requestslib_kwargs=None):
        """
        @summary: Sets the power state for a node.
        @param uuid: The uuid of an existing node.
        @type uuid: String
        @param state: The desired state for the node.
        @type state: String
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/nodes/{uuid}/states/power'.format(
            base_url=self.url, uuid=uuid)
        request = SetNodePowerState(power_state=state)
        resp = self.post(url, request_entity=request,
                         requestslib_kwargs=requestslib_kwargs)
        return resp

    def set_node_console_mode(self, uuid, enabled, requestslib_kwargs=None):
        """
        @summary: Activates or deactivates console mode for a node.
        @param uuid: The uuid of an existing node.
        @type uuid: String
        @param enabled: Determines if console mode is enabled or not.
        @type enabled: Boolean
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/nodes/{uuid}/states/console'.format(
            base_url=self.url, uuid=uuid)
        request = SetNodeConsoleMode(enabled=enabled)
        resp = self.post(url, request_entity=request,
                         requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_console_for_node(self, uuid, requestslib_kwargs=None):
        """
        @summary: Returns a console for a node.
        @param uuid: The uuid of an existing node
        @type uuid: String
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/nodes/{uuid}/states/console'.format(
            base_url=self.url, uuid=uuid)

        # TODO(dwalleck): Add response type once this request can be attempted
        resp = self.get(url, requestslib_kwargs=requestslib_kwargs)
        return resp

    def validate_node(self, uuid, requestslib_kwargs=None):
        """
        @summary: Returns the driver interfaces of a node.
        @param uuid: The uuid of an existing node
        @type uuid: String
        @return: resp
        @rtype: Requests.response
        """
        url = '{base_url}/nodes/{uuid}/validate'.format(
            base_url=self.url, uuid=uuid)
        resp = self.get(url, response_entity_type=DriverInterfaces,
                        requestslib_kwargs=requestslib_kwargs)
        return resp

    def update_node(self, uuid, patches, requestslib_kwargs=None):
        """
        @summary: Updates the properties of a node with the provided patch.
        @param uuid: The uuid of an existing node.
        @type uuid: String
        @param patches: List of patches to update the node with.
        @type patches: List of Dict
        @return: resp
        @rtype: Requests.response
        """

        url = '{base_url}/nodes/{uuid}'.format(base_url=self.url, uuid=uuid)
        request = Patches(patches=patches)
        resp = self.patch(url,
                          response_entity_type=Node,
                          request_entity=request,
                          requestslib_kwargs=requestslib_kwargs)
        return resp
