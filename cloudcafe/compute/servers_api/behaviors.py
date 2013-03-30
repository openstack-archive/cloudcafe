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

import time

from cloudcafe.compute.common.types import NovaServerStatusTypes as ServerStates
from cloudcafe.compute.common.datagen import rand_name
from cloudcafe.compute.common.exceptions import ItemNotFound, \
    TimeoutException, BuildErrorException


class ServerBehaviors(object):

    def __init__(self, servers_client, servers_config,
                 images_config, flavors_config):

        self.config = servers_config
        self.servers_client = servers_client
        self.images_config = images_config
        self.flavors_config = flavors_config

    def create_active_server(self, name=None, image_ref=None, flavor_ref=None,
                             personality=None, metadata=None, accessIPv4=None,
                             accessIPv6=None, disk_config=None, networks=None):
        '''
        @summary:Creates a server and waits for server to reach active status
        @param name: The name of the server.
        @type name: String
        @param image_ref: The reference to the image used to build the server.
        @type image_ref: String
        @param flavor_ref: The flavor used to build the server.
        @type flavor_ref: String
        @param metadata: A dictionary of values to be used as metadata.
        @type metadata: Dictionary. The limit is 5 key/values.
        @param personality: A list of dictionaries for files to be
         injected into the server.
        @type personality: List
        @param accessIPv4: IPv4 address for the server.
        @type accessIPv4: String
        @param accessIPv6: IPv6 address for the server.
        @type accessIPv6: String
        @param disk_config: MANUAL/AUTO/None
        @type disk_config: String
        @return: Response Object containing response code and
         the server domain object
        @rtype: Request Response Object
        '''

        if name is None:
            name = rand_name('testserver')
        if image_ref is None:
            image_ref = self.images_config.primary_image
        if flavor_ref is None:
            flavor_ref = self.flavors_config.primary_flavor

        resp = self.servers_client.create_server(name, image_ref,
                                                 flavor_ref,
                                                 personality=personality,
                                                 metadata=metadata,
                                                 accessIPv4=accessIPv4,
                                                 accessIPv6=accessIPv6,
                                                 disk_config=disk_config,
                                                 networks=networks)
        server_obj = resp.entity
        resp = self.wait_for_server_status(server_obj.id,
                                           ServerStates.ACTIVE)
        # Add the password from the create request into the final response
        resp.entity.admin_pass = server_obj.admin_pass
        return resp

    def wait_for_server_status(self, server_id, desired_status, timeout=None):
        """Polls server until the desired status is reached"""
        if desired_status == ServerStates.DELETED:
            return self.wait_for_server_to_be_deleted(server_id)
        server_response = self.servers_client.get_server(server_id)
        server_obj = server_response.entity
        time_waited = 0
        interval_time = self.config.server_status_interval
        timeout = timeout or self.config.server_build_timeout
        while (server_obj.status.lower() != desired_status.lower() and
               server_obj.status.lower() != ServerStates.ERROR.lower() and
               time_waited <= timeout):
            server_response = self.servers_client.get_server(server_id)
            server_obj = server_response.entity
            time.sleep(interval_time)
            time_waited += interval_time
        if time_waited > timeout:
            raise TimeoutException
        if server_obj.status.lower() == ServerStates.ERROR.lower():
            raise BuildErrorException(
                'Build failed. Server with uuid %s entered ERROR status.' %
                (server_id))
        return server_response

    def wait_for_server_error_status(self, server_id, desired_status,
                                     timeout=None):
        """Polls a server until the desired status is reached"""

        if desired_status == ServerStates.DELETED:
            return self.wait_for_server_to_be_deleted(server_id)
        server_response = self.servers_client.get_server(server_id)
        server_obj = server_response.entity
        time_waited = 0
        interval_time = self.config.server_status_interval
        timeout = timeout or self.config.compute_api.server_status_timeout
        while (server_obj.status.lower() != desired_status.lower()
               and time_waited <= timeout * 10):
            server_response = self.servers_client.get_server(server_id)
            server_obj = server_response.entity
            time.sleep(interval_time)
            time_waited += interval_time
        return server_response

    def wait_for_server_status_from_error(self, server_id, desired_status,
                                          timeout=None):
        if desired_status == ServerStates.DELETED:
            return self.wait_for_server_to_be_deleted(server_id)
        server_response = self.servers_client.get_server(server_id)
        server_obj = server_response.entity
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        timeout = timeout or self.config.compute_api.server_status_timeout
        while (server_obj.status.lower() != desired_status.lower()
               and time_waited <= timeout):
            server_response = self.servers_client.get_server(server_id)
            server_obj = server_response.entity
            time.sleep(interval_time)
            time_waited += interval_time
        if time_waited > timeout:
            raise TimeoutException(server_obj.status, server_obj.status,
                                   id=server_obj.id)
        return server_response

    def wait_for_server_to_be_deleted(self, server_id):
        time_waited = 0
        interval_time = self.config.server_status_interval
        try:
            while (True):
                server_response = self.servers_client.get_server(server_id)
                server_obj = server_response.entity
                if time_waited > self.config.server_build_timeout:
                    raise TimeoutException(
                        "Timed out while deleting server id: %s" % server_id)
                if server_obj.status.lower() != ServerStates.ERROR.lower():
                    time.sleep(interval_time)
                    time_waited += interval_time
                    continue
                    if server_obj.status.lower() != ServerStates.ERROR.lower():
                        raise BuildErrorException(
                            "Server entered Error state while deleting, \
                            server id : %s" % server_id)
                time.sleep(interval_time)
                time_waited += interval_time
        except ItemNotFound:
            pass

    def resize_and_await(self, server_id, new_flavor):
        resp = self.servers_client.resize(server_id, new_flavor)
        assert resp.status_code is 202
        resized_server = self.wait_for_server_status(
            server_id, ServerStates.VERIFY_RESIZE)
        return resized_server.entity

    def resize_and_confirm(self, server_id, new_flavor):
        self.resize_and_await(server_id, new_flavor)
        resp = self.servers_client.confirm_resize(server_id)
        assert resp.status_code is 204
        resized_server = self.wait_for_server_status(server_id,
                                                     ServerStates.ACTIVE)
        return resized_server.entity

    def resize_and_revert(self, server_id, new_flavor):
        self.resize_and_await(server_id, new_flavor)
        resp = self.servers_client.revert_resize(server_id)
        assert resp.status_code is 202
        resized_server = self.wait_for_server_status(server_id,
                                                     ServerStates.ACTIVE)
        return resized_server.entity

    def reboot_and_await(self, server_id, reboot_type):
        resp = self.servers_client.reboot(server_id, reboot_type)
        assert resp.status_code is 202
        self.wait_for_server_status(server_id,
                                    ServerStates.ACTIVE)

    def change_password_and_await(self, server_id, new_password):
        resp = self.servers_client.change_password(server_id, new_password)
        assert resp.status_code is 202
        self.wait_for_server_status(server_id,
                                    ServerStates.ACTIVE)
