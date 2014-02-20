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

import base64
import time

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.compute.common.clients.remote_instance.linux.linux_client \
    import LinuxClient
from cloudcafe.compute.common.types import InstanceAuthStrategies
from cloudcafe.compute.common.types import NovaServerStatusTypes \
    as ServerStates
from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.compute.common.exceptions import ItemNotFound, \
    TimeoutException, BuildErrorException, RequiredResourceException


class ServerBehaviors(BaseBehavior):

    def __init__(self, servers_client, servers_config,
                 images_config, flavors_config,
                 block_device_mapping, volumes_client=None,
                 blockstorage_behavior=None):

        super(ServerBehaviors, self).__init__()
        self.config = servers_config
        self.servers_client = servers_client
        self.images_config = images_config
        self.flavors_config = flavors_config
        self.block_device_mapping = block_device_mapping
        self.volumes_client = volumes_client

    def create_active_server(
            self, name=None, image_ref=None, flavor_ref=None,
            personality=None, user_data=None, metadata=None,
            accessIPv4=None, accessIPv6=None, disk_config=None,
            networks=None, key_name=None, config_drive=None,
            scheduler_hints=None, admin_pass=None,
            block_device_mapping=None):
        """
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
        @param user_data: Config Init User data
        @type user_data: String
        @param config_drive: Config Drive flag
        @type config_drive: String
        @param accessIPv4: IPv4 address for the server.
        @type accessIPv4: String
        @param accessIPv6: IPv6 address for the server.
        @type accessIPv6: String
        @param disk_config: MANUAL/AUTO/None
        @type disk_config: String
        @return: Response Object containing response code and
         the server domain object
        @rtype: Request Response Object
        """

        if name is None:
            name = rand_name('testserver')
        if image_ref is None and block_device_mapping is None:
            image_ref = self.images_config.primary_image
        if flavor_ref is None:
            flavor_ref = self.flavors_config.primary_flavor

        failures = []
        attempts = self.config.resource_build_attempts
        for attempt in range(attempts):

            self._log.debug('Attempt {attempt} of {attempts} '
                            'to create server.'.format(attempt=attempt + 1,
                                                       attempts=attempts))
            resp = self.servers_client.create_server(
                name, image_ref, flavor_ref, personality=personality,
                config_drive=config_drive, metadata=metadata,
                accessIPv4=accessIPv4, accessIPv6=accessIPv6,
                disk_config=disk_config, networks=networks, key_name=key_name,
                scheduler_hints=scheduler_hints, user_data=user_data,
                admin_pass=admin_pass,
                block_device_mapping=block_device_mapping)
            server_obj = resp.entity

            try:
                resp = self.wait_for_server_status(
                    server_obj.id, ServerStates.ACTIVE)
                # Add the password from the create request
                # into the final response
                resp.entity.admin_pass = server_obj.admin_pass
                return resp
            except (TimeoutException, BuildErrorException) as ex:
                self._log.error('Failed to build server {server_id}: '
                                '{message}'.format(server_id=server_obj.id,
                                                   message=ex.message))
                failures.append(ex.message)
                self.servers_client.delete_server(server_obj.id)

        raise RequiredResourceException(
            'Failed to successfully build a server after '
            '{attempts} attempts: {failures}'.format(
                attempts=attempts, failures=failures))

    def wait_for_server_status(self, server_id, desired_status,
                               interval_time=None, timeout=None):
        """
        @summary: Waits for a server to reach a desired status
        @param server_id: The uuid of the server
        @type server_id: String
        @param desired_status: The desired final status of the server
        @type desired_status: String
        @param interval_time: The amount of time in seconds to wait
                              between polling
        @type interval_time: Integer
        @param interval_time: The amount of time in seconds to wait
                              before aborting
        @type interval_time: Integer
        @return: Response object containing response and the server
                 domain object
        @rtype: requests.Response
        """

        interval_time = interval_time or self.config.server_status_interval
        timeout = timeout or self.config.server_build_timeout
        end_time = time.time() + timeout

        time.sleep(interval_time)
        while time.time() < end_time:
            resp = self.servers_client.get_server(server_id)
            server = resp.entity

            if server.status.lower() == ServerStates.ERROR.lower():
                raise BuildErrorException(
                    'Build failed. Server with uuid %s entered ERROR status.'
                    % server.id)

            if server.status == desired_status:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait_for_server_status ran for {0} seconds and did not "
                "observe server {1} reach the {2} status.".format(
                    timeout, server_id, desired_status))

        return resp

    def wait_for_server_to_be_deleted(self, server_id, interval_time=None,
                                      timeout=None):
        """
        @summary: Waits for a server to be deleted
        @param server_id: The uuid of the server
        @type server_id: String
        @param interval_time: The amount of time in seconds to wait
                              between polling
        @type interval_time: Integer
        @param timeout: The amount of time in seconds to wait
                              before aborting
        @type timeout: Integer
        """

        interval_time = interval_time or self.config.server_status_interval
        timeout = timeout or self.config.server_build_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            try:
                self.servers_client.get_server(server_id)
            except ItemNotFound:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait_for_server_status ran for {0} seconds and did not "
                "observe the server achieving the {1} status.".format(
                    timeout, 'DELETED'))

    def confirm_server_deletion(self, server_id, response_code,
                                interval_time=None, timeout=None):
        """
        @summary: confirm server deletion based on response code.
        @param server_id: The uuid of the server
        @type server_id: String
        @param: response code to wait for to confirm server deletion
        @type: Integer
        @param interval_time: The amount of time in seconds to wait
                              between polling
        @type interval_time: Integer
        @param timeout: The amount of time in seconds to wait
                              before aborting
        @type timeout: Integer
        """
        interval_time = interval_time or self.config.server_status_interval
        timeout = timeout or self.config.server_build_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            resp = self.servers_client.get_server(server_id)
            if resp.status_code == response_code:
                return
            time.sleep(interval_time)
        raise TimeoutException(
            "wait_for_server_status ran for {0} seconds and did not "
            "observe the server achieving the {1} status based on "
            "response code.".format(timeout, 'DELETED'))

    def get_public_ip_address(self, server):
        """
        @summary: Gets the public ip address of instance
        @param server: Instance uuid id of the server
        @type server: String
        @return: Either IPv4 or IPv6 address of instance
        @rtype: String
        """
        if self.config.ip_address_version_for_ssh == '4':
            return server.addresses.public.ipv4
        else:
            return server.addresses.public.ipv6

    def get_remote_instance_client(self, server, config=None, ip_address=None,
                                   username=None, password=None, key=None,
                                   auth_strategy=None):
        """
        @summary: Gets an client of the server
        @param server: Instance uuid id of the server
        @type server: String
        @param ip_address: IPv4 address of the server
        @type ip_address: String
        @param username: Valid user of the server
        @type username: String
        @param password: Valid user password of the server
        @type password: String
        @return: Either IPv4 or IPv6 address of instance
        @rtype: String
        """

        if ip_address is None:
            ip_address = self.get_public_ip_address(server)

        strategy = auth_strategy or self.config.instance_auth_strategy.lower()

        if InstanceAuthStrategies.PASSWORD in strategy:

            if password is None:
                password = server.admin_pass

            # (TODO) dwalleck: Remove hard coding of distro
            return LinuxClient(ip_address=ip_address, username='root',
                               password=password)
            #return InstanceClientFactory.get_instance_client(
            #    ip_address=ip_address, username=username, password=password,
            #    os_distro='linux', config=config)
        else:
            return LinuxClient(ip_address=ip_address, username='root', key=key)
            #return InstanceClientFactory.get_instance_client(
            #    ip_address=ip_address, username=username, os_distro='linux',
            #    config=config, key=key)

    def resize_and_await(self, server_id, new_flavor):
        """
        @summary: Resizes a server and waits for VERIFY_RESIZE status
        @param server_id: The uuid of the server
        @type server_id: String
        @param new_flavor: The flavor to resize a server to
        @type new_flavor: String
        @return: The Server after the resize has completed
        @rtype: Server
        """

        resp = self.servers_client.resize(server_id, new_flavor)
        assert resp.status_code is 202
        resized_server = self.wait_for_server_status(
            server_id, ServerStates.VERIFY_RESIZE)
        return resized_server.entity

    def resize_and_confirm(self, server_id, new_flavor):
        """
        @summary: Resizes a server, confirms, and waits for the
                  confirmation to complete
        @param server_id: The uuid of the server
        @type server_id: String
        @param new_flavor: The flavor to resize a server to
        @type new_flavor: String
        @return: The Server after the resize has been confirmed
        @rtype: Server
        """

        self.resize_and_await(server_id, new_flavor)
        resp = self.servers_client.confirm_resize(server_id)
        assert resp.status_code is 204
        resized_server = self.wait_for_server_status(server_id,
                                                     ServerStates.ACTIVE)
        return resized_server.entity

    def resize_and_revert(self, server_id, new_flavor):
        """
        @summary: Resizes a server, reverts the resize, and waits for the
                  revert to complete
        @param server_id: The uuid of the server
        @type server_id: String
        @param new_flavor: The flavor to resize a server to
        @type new_flavor: String
        @return: The Server after the resize has been reverted
        @rtype: Server
        """

        self.resize_and_await(server_id, new_flavor)
        resp = self.servers_client.revert_resize(server_id)
        assert resp.status_code is 202
        resized_server = self.wait_for_server_status(server_id,
                                                     ServerStates.ACTIVE)
        return resized_server.entity

    def reboot_and_await(self, server_id, reboot_type):
        """
        @summary: Reboots a server and waits for the action to complete
        @param server_id: The uuid of the server
        @type server_id: String
        @param reboot_type: The type of reboot to perform
        @type reboot_type: String
        @return: The Server after the reboot has completed
        @rtype: Server
        """

        resp = self.servers_client.reboot(server_id, reboot_type)
        assert resp.status_code is 202
        resp = self.wait_for_server_status(server_id,
                                           ServerStates.ACTIVE)
        return resp.entity

    def change_password_and_await(self, server_id, new_password):
        """
        @summary: Changes the server password and waits for
                  the action to complete
        @param server_id: The uuid of the server
        @type server_id: String
        @param new_password: The new server password
        @type new_password: String
        @return: The Server after the password has been changed
        @rtype: Server
        """

        resp = self.servers_client.change_password(server_id, new_password)
        assert resp.status_code is 202
        resp = self.wait_for_server_status(server_id,
                                           ServerStates.ACTIVE)
        return resp.entity

    def boot_volume(self, key=None, trigger_value=None,
                    standard_volume_id=None, user_data=None):
        """
        @summary: Allow the ability to build a volume and then a server
                  of build a server based on config file parms
        @return: The server and the volume entity
        @rtype: Server object, volume object
        """
        self.volume_id = self.block_device_mapping.bdm_volume_id
        if standard_volume_id is not None:
            self.volume_id = standard_volume_id
        volume_response = ""
        if self.block_device_mapping.bdm_boot_type == "B":
            if self.volume_id < " ":
                """create volume"""
                volume_response = self.create_boot_volume()
            else:
                volume_response = self.volume_id
        self.trigger_value = trigger_value
        self.user_data = user_data
        """ Create server"""
        response = self.create_boot_server(volume_response, key,
                                           self.trigger_value, self.user_data)
        return response, self.volume_id

    def create_boot_volume(self):
        """
        @summary: create a bootable volume
        @return: The volume entity
        @rtype: volume object
        """
        self.volume_name = rand_name("bootable_volume")
        self.volume_size = self.block_device_mapping.bdm_volume_size
        self.vol_type = self.block_device_mapping.bdm_volume_type
        self.volume_image = self.block_device_mapping.bdm_volume_image
        volume = self.volumes_client.create_volume(
            self.volume_size, self.vol_type, 
            name=self.volume_name, image_ref=self.volume_image)
        volume_id = volume.entity
        resp = self.volumes_client.get_volume_info(volume_id=volume_id.id_)
        while resp.entity.status != "available":
            resp = self.volumes_client.get_volume_info(volume_id=volume_id.id_)
        return volume_id

    def create_boot_server(self, volume_id, key, trigger_value=None,
                           user_data=None):
        """
        @parm volume_id: volume entity
        @type: volume object
        @parm key: keypair for server
        @type: string
        @parm trigger_value: value indicating variable to tested
        @type: string
        @parm user_data: passed value for cloud init
        @type: string
        @summary: create a server with or without a bootable volume
        @return: The server object
        @rtype: server object
        """
        self.trigger_value = trigger_value
        self.volume_id = volume_id
        self.name = rand_name("server")
        self.metadata = {'meta_key_1': 'meta_value_1',
                         'meta_key_2': 'meta_value_2'}
        self.file_contents = 'This is a config drive test file.'
        files = [{'path': '/test.txt', 'contents': base64.b64encode(
            self.file_contents)}]
        if user_data is None:
            self.user_data_contents = "My user data"
            self.user_data = base64.b64encode(self.user_data_contents)
            self.config_drive = False
        else:
            self.user_data = user_data
            self.config_drive = True
        self.key = key
        self.flavor_ref = None
        self.block_device_mapping_values = None

        if self.block_device_mapping.bdm_boot_type == "B":
            self.del_on_term = (
                self.block_device_mapping.bdm_delete_on_termination)
            self.devname = self.block_device_mapping.bdm_devname
            self.size = self.block_device_mapping.bdm_size
            self.type = self.block_device_mapping.bdm_type
            """
            NDN - Negative Device Name
            NTV - Negative Type Value
            NDOT = Negative Delete on Termination
            NVI - Negative Invalid Volume id
            NDV - Negative Deleted Volume
            NFV - Negative Flavor Value
            PDN - Postive Do Not delete on Termination
            PDT - Positive delete on Termination
            """
            if trigger_value == "PDN":
                self.del_on_term = False
            if trigger_value == "PDT":
                self.del_on_term = True
            if trigger_value == "NDN":
                self.devname = "XXX"
            if trigger_value == "NTV":
                self.type = "XXX"
            if trigger_value == "NDOT":
                self.del_on_term = "XXX"
            if trigger_value == "NVI":
                self.volume_id.id_ = "XXX"
            if trigger_value == "NFV":
                self.flavor_ref = "XXX"
            if trigger_value == "NDV":
                self.volume_id.id_ = "33ac75ff-4bd8-4640-82b9-1f023d4e2cfd"
            self.block_device_mapping_values = [
                {"volume_id": self.volume_id.id_,
                 "delete_on_termination": self.del_on_term,
                 "device_name": self.devname,
                 "size": self.size,
                 "type": self.type}]
        response = self.create_active_server(
            flavor_ref=self.flavor_ref,
            config_drive=self.config_drive,
            key_name=self.key.name, metadata=self.metadata,
            user_data=self.user_data, personality=files,
            block_device_mapping=self.block_device_mapping_values)
        return response
