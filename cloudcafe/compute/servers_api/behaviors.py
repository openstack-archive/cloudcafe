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
import re

from cloudcafe.common.behaviors import (
    StatusProgressionVerifier, StatusProgressionError, StatusPollError)
from cloudcafe.compute.common.behaviors import BaseComputeBehavior
from cloudcafe.compute.common.constants import HTTPResponseCodes
from cloudcafe.compute.common.types import InstanceAuthStrategies
from cloudcafe.compute.common.types import NovaServerStatusTypes \
    as ServerStates
from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.compute.common.exceptions import ItemNotFound, \
    TimeoutException, BuildErrorException, SshConnectionException


class ServerBehaviors(BaseComputeBehavior):

    def __init__(self, servers_client, images_client, servers_config,
                 images_config, flavors_config, boot_from_volume_client=None,
                 security_groups_config=None):
        super(ServerBehaviors, self).__init__()
        self.config = servers_config
        self.servers_client = servers_client
        self.images_client = images_client
        self.images_config = images_config
        self.flavors_config = flavors_config
        self.boot_from_volume_client = boot_from_volume_client
        self.security_groups_config = security_groups_config

    def create_server_with_defaults(
            self, name=None, name_prefix=None, image_ref=None, flavor_ref=None,
            personality=None, user_data=None, metadata=None,
            accessIPv4=None, accessIPv6=None, disk_config=None,
            networks=None, key_name=None, config_drive=None,
            scheduler_hints=None, admin_pass=None, max_count=None,
            min_count=None, block_device_mapping=None, security_groups=None):
        """
        @summary:Creates a server using any configured default values
        @param name: The name of the server.
        @type name: String
        @param name_prefix: The prefix used for the randomized server name.
        @type name_prefix: String
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
        @parm block_device_mapping:fields needed to boot a server from a volume
        @type block_device_mapping: dict
        @param security_groups: List of security groups for the server
        @type security_groups: List of dict
        @return: Response Object containing response code and
                 the server domain object
        @rtype: Request Response Object
        """

        if name is None:
            name = rand_name(name_prefix or 'testserver')
        if image_ref is None and block_device_mapping is None:
            image_ref = self.images_config.primary_image
        if flavor_ref is None:
            flavor_ref = self.flavors_config.primary_flavor
        if self.config.default_network:
            networks = [{'uuid': self.config.default_network}]

        # If default scheduler hints are set, add them to the request
        if self.config.default_scheduler_hints:
            if scheduler_hints:
                scheduler_hints.update(self.config.default_scheduler_hints)
            else:
                scheduler_hints = self.config.default_scheduler_hints

        default_files = self.get_default_injected_files()

        if personality and default_files:
            personality += default_files
        else:
            personality = personality or default_files

        default_groups = None
        if (self.security_groups_config
                and self.security_groups_config.default_security_group):
            default_groups = [
                {"name": self.security_groups_config.default_security_group}]

        if default_groups and security_groups:
            security_groups.extend(default_groups)
        else:
            security_groups = security_groups or default_groups

        kwargs = None
        if (self.config.default_scheduler_hints and
            self.config.scheduler_hints_url):
                # Extract tenant id from the url
                tenant_id = re.findall('\d+', self.servers_client.url)[1]
                # Replace Create Server url only with that from scheduler hints
                client_url = '{0}/{1}'.format(
                    self.config.scheduler_hints_url.rstrip('/'),
                    tenant_id)
                bypass_url = '{client_url}/servers'.format(client_url=client_url)
                kwargs = {'url': bypass_url}

        response = self.servers_client.create_server(
            name, image_ref, flavor_ref, personality=personality,
            config_drive=config_drive, metadata=metadata,
            accessIPv4=accessIPv4, accessIPv6=accessIPv6,
            disk_config=disk_config, networks=networks,
            scheduler_hints=scheduler_hints, user_data=user_data,
            admin_pass=admin_pass, key_name=key_name,
            block_device_mapping=block_device_mapping,
            security_groups=security_groups, requestslib_kwargs=kwargs)
        self.verify_entity(response)
        return response

    def wait_for_server_creation(self, server_id):
        """
        @summary: Waits for a server to be created successfully
        @param server_id: The uuid of the server
        @type server_id: String
        @return: A server object after it has been successfully built
        @rtype: Server
        """

        verifier = StatusProgressionVerifier(
            'server', server_id,
            lambda id_: self.verify_entity(
                self.servers_client.get_server(id_)).status,
            server_id)

        retry_limit = self.config.server_status_poll_failure_max_retries
        verifier.set_global_state_properties(
            timeout=self.config.server_build_timeout)
        verifier.add_state(
            expected_statuses=[ServerStates.BUILD],
            acceptable_statuses=[ServerStates.ACTIVE],
            error_statuses=[ServerStates.ERROR],
            poll_rate=self.config.server_status_interval,
            poll_failure_retry_limit=retry_limit)

        verifier.add_state(
            expected_statuses=[ServerStates.ACTIVE],
            error_statuses=[ServerStates.ERROR],
            poll_rate=self.config.server_status_interval,
            poll_failure_retry_limit=retry_limit)

        try:
            verifier.start()
        except (StatusProgressionError, StatusPollError) as e:
            if not e.args:
                e.args=('',)
            e.args = (
                'Failed to create server with instance '
                'id {id}'.format(id=server_id),) + e.args
            e.args = ('; '.join(e.args),)
            raise
        except Exception as e:
            if not e.args:
                e.args=('',)
            e.args = (
                'Unexpected error occurred while waiting for server {id}'
                'to be created.'.format(id=server_id),) + e.args
            e.args = ('; '.join(e.args),)
            raise

        response = self.servers_client.get_server(server_id)
        return self.verify_entity(response)

    def create_active_server(
            self, name=None, image_ref=None, flavor_ref=None, personality=None,
            user_data=None, metadata=None, accessIPv4=None, accessIPv6=None,
            disk_config=None, networks=None, key_name=None, config_drive=None,
            scheduler_hints=None, admin_pass=None, max_count=None,
            min_count=None, block_device_mapping=None, security_groups=None,
            name_prefix=None):
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
        @parm block_device_mapping:fields needed to boot a server from a volume
        @type block_device_mapping: dict
        @param security_groups: List of security groups for the server
        @type security_groups: List of dict
        @return: Response Object containing response code and
                 the server domain object
        @rtype: Request Response Object
        @param name_prefix: The prefix to be used for the randomized server name.
        @type name_prefix: String
        """

        create_response = self.create_server_with_defaults(
            name=name, name_prefix=name_prefix, image_ref=image_ref,
            flavor_ref=flavor_ref, personality=personality,
            config_drive=config_drive, metadata=metadata,
            accessIPv4=accessIPv4, accessIPv6=accessIPv6,
            disk_config=disk_config, networks=networks,
            scheduler_hints=scheduler_hints, user_data=user_data,
            admin_pass=admin_pass, key_name=key_name,
            block_device_mapping=block_device_mapping,
            security_groups=security_groups)
        server = create_response.entity

        try:
            built_server = self.wait_for_server_creation(server.id)
        except Exception:
            if not self.config.keep_resources_on_failure:
                self.servers_client.delete_server(server.id)
            raise

        built_server.admin_pass = server.admin_pass
        create_response.entity = built_server
        return create_response

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
        @param timeout: The amount of time in seconds to wait
                              before aborting
        @type timeout: Integer
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
            server = self.verify_entity(resp)

            if server.status.lower() == ServerStates.ERROR.lower():
                raise BuildErrorException(
                    "Build failed. Server with uuid {server_id} entered "
                    "ERROR status.".format(server_id=server.id))

            if server.status == desired_status:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait_for_server_status ran for {0} seconds and did not "
                "observe server {1} reach the {2} status.".format(
                    timeout, server_id, desired_status))

        return resp

    def wait_for_server_task_state(self, server_id, state_to_wait_for,
                                   timeout, interval_time=None):
        """
        @summary: Polls server task state until state_to_wait_for is met
        @param server_id: The uuid of the server
        @type server_id: String
        @param state_to_wait_for: The desired final status of the server
        @type state_to_wait_for: String
        @param timeout: The amount of time in seconds to wait
                              before aborting
        @type timeout: Integer
        @param interval_time: The amount of time in seconds to wait
                              between polling
        @type interval_time: Integer
        """

        if state_to_wait_for is not None:
            state_to_wait_for = state_to_wait_for.lower()

        interval_time = interval_time or self.config.server_status_interval
        end_time = time.time() + timeout

        while time.time() < end_time:
            response = self.servers_client.get_server(server_id)
            self.verify_entity(response)
            task_state = response.entity.task_state.lower()

            if response.entity.status.lower() == ServerStates.ERROR.lower():
                raise BuildErrorException(
                    "Build failed. Server with uuid {server_id} entered "
                    "ERROR status.".format(server_id=server_id))

            if task_state == state_to_wait_for:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "Wait for server task ran for {timeout} seconds and did not "
                "observe server {server_id} reach desired task state of "
                "{state_to_wait_for}."
                .format(timeout=timeout, server_id=server_id,
                        state_to_wait_for=state_to_wait_for))
        return response

    def wait_for_metadata_value(self, server_id, metadata_key,
                                potential_values, timeout, interval_time=None):
        """
        @summary: Polls a server's metadata for a specific key until it
                  reaches one of the specified values or times out
        @param server_id: The uuid of the server
        @type server_id: String
        @param metadata_key: Metadata key to poll for desired value
        @type metadata_key: String
        @param potential_values: A list of potential values that are
                                 actionable. If the metadata key reaches any
                                 of the values in this list, the method should
                                 return that value and exit.
        @type potential_values: List of Strings
        @param interval_time: The amount of time in seconds to wait
                              between polling.
        @type interval_time: Integer
        @param timeout: The amount of time in seconds to wait before aborting.
        @type timeout: Integer
        @return: The final value of the metadata_key, either a specified value
                 or the value of the key at timeout
        @rtype: String
        """
        interval_time = interval_time or self.config.server_status_interval
        end_time = time.time() + timeout
        metadata_value = None

        while time.time() < end_time:
            response = self.servers_client.list_server_metadata(server_id)
            metadata = self.verify_entity(response)

            # Key may not exist yet, so check before accessing
            if metadata_key in metadata:
                metadata_value = metadata[metadata_key]
                if metadata_value in potential_values:
                    return metadata_value
            time.sleep(interval_time)

        # Raise an exception if metadata didn't reach desired value within
        # the timeout interval
        if metadata_value:
            metadata_result = "Key {0} ended with value {1}".format(
                metadata_key, metadata_value)
        else:
            metadata_result = "Key {0} was not found.".format(metadata_key)

        raise TimeoutException(
            "wait_for_metadata_value ran for {timeout} seconds and did not "
            "observe server {server_id} reach any of the specified values, "
            "{potential_values}, for metadata key {metadata_key}. {result}"
            .format(
                timeout=timeout, server_id=server_id,
                potential_values=potential_values, metadata_key=metadata_key,
                result=metadata_result))

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
                resp = self.servers_client.get_server(server_id)
                if resp.status_code == HTTPResponseCodes.NOT_FOUND:
                    break
            except ItemNotFound:
                break
            time.sleep(interval_time)
        else:
            msg = ('wait_for_server_to_be_deleted {0} seconds timeout waiting'
                   'for the expected get server HTTP {1} status code').format(
                       timeout, HTTPResponseCodes.NOT_FOUND)
            raise TimeoutException(msg)

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
            "the expected response code: {2}.".format(
                timeout, 'DELETED', response_code))

    def get_default_injected_files(self):
        """
        @summary: Checks for and returns a list of default injected files
        @return: List of dictionaries containing a default injected file
                 path and its encoded contents
        @rtype: List
        """
        if self.config.default_injected_files:
            # Encode the file contents
            default_files = self.config.default_injected_files
            for personality_file in default_files:
                personality_file['contents'] = base64.b64encode(
                    personality_file['contents'])
            return default_files
        else:
            return None

    def get_public_ip_address(self, server):
        """
        @summary: Gets the public ip address of instance
        @param server: Instance uuid id of the server
        @type server: String
        @return: Either IPv4 or IPv6 address of instance
        @rtype: String
        """
        if self.config.ip_address_version_for_ssh == 4:
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
            network = server.addresses.get_by_name(config.network_for_ssh)
            if config.ip_address_version_for_ssh == 4:
                ip_address = network.ipv4
            elif config.ip_address_version_for_ssh == 6:
                ip_address = network.ipv6

        # Get Server Image ID
        if server.image:
            image_id = server.image.id
        else:
            image_id = self.images_config.primary_image

        # Get the Server Image
        image = self.images_client.get_image(image_id).entity

        if image.metadata.get('os_type', '').lower() == 'windows':
            # Importing just in time in case WinRM plugin is not installed
            # (todo) dwalleck: Handle this more cleanly
            from cloudcafe.compute.common.clients.remote_instance.windows.\
                windows_client import WindowsClient
            client = WindowsClient
        else:
            # Importing just in time in case SSH plugin is not installed
            # (todo) dwalleck: Handle this more cleanly
            from cloudcafe.compute.common.clients.remote_instance.linux.\
                linux_client import LinuxClient
            client = LinuxClient

        user = username or self.images_config.primary_image_default_user
        strategy = auth_strategy or self.config.instance_auth_strategy.lower()

        try:
            if InstanceAuthStrategies.PASSWORD in strategy:
                if password is None:
                    password = server.admin_pass
                return client(
                    ip_address=ip_address, username=user, password=password,
                    connection_timeout=self.config.connection_timeout)
            else:
                return client(
                    ip_address=ip_address, username=user, key=key,
                    connection_timeout=self.config.connection_timeout)
        except TimeoutException:
            raise TimeoutException(
                'Unable to ping server {id} at address {address} '
                'within the allowed time of {timeout} seconds. '
                'Test unable to proceed.'.format(
                    id=server.id, address=ip_address,
                    timeout=self.config.connection_timeout))
        except SshConnectionException:
            raise SshConnectionException(
                'Able to ping server {id} at {address}, but unable to '
                'connect via ssh within the allowed time of {timeout} '
                'seconds. Test unable to proceed.'.format(
                    id=server.id, address=ip_address,
                    timeout=self.config.connection_timeout))

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
        resp.entity.admin_pass = new_password
        return resp.entity

    def create_block_device_mapping_v1(self, volume_id, delete_on_termination,
                                       device_name, size, type):
        """
        @summary: Creates Block Device mapping on the fly
        @param volume_id: The uuid of the volume
        @type volume_id: String
        @param delete_on_termination:  True or False also 0 or 1
        @type delete_on_termination: Boolean
        @param device_name: Device name
        @type device_name: String
        @param size: Volume Size in GB
        @type size: Int
        @param type: snap or blank, from where the volume was created
        @type type: String
        @return: The Block Device Mapping
        @rtype: List of dicts
        """

        # Creating block device mapping
        block_device_mapping_matrix = [{
            "volume_id": volume_id,
            "delete_on_termination": delete_on_termination,
            "device_name": device_name,
            "size": size,
            "type": type}]
        return block_device_mapping_matrix

    def create_block_device_mapping_v1_virt2837(self, device_name, volume_id, delete_on_termination):
        """
        @summary: Creates Block Device mapping on the fly
        @param volume_id: The uuid of the volume
        @type volume_id: String
        @param delete_on_termination:  True or False also 0 or 1
        @type delete_on_termination: Boolean
        @param device_name: Device name
        @type device_name: String
        @param size: Volume Size in GB
        @type size: Int
        @param type: snap or blank, from where the volume was created
        @type type: String
        @return: The Block Device Mapping
        @rtype: List of dicts
        """

        # Creating block device mapping
        block_device_mapping_matrix = [{
            "device_name": device_name,
            "volume_id": volume_id,
            "delete_on_termination": delete_on_termination}]
        return block_device_mapping_matrix

    def create_block_device_mapping_v2(self, boot_index, uuid, volume_size,
                                       source_type, destination_type,
                                       delete_on_termination):
        """
        @summary: Creates Block Device on the fly
        @param uuid: The uuid of the volume
        @type uuid: String
        @param delete_on_termination:  True or False also 0 or 1
        @type delete_on_termination: Boolean
        @param boot_index: Used to order the boot disks
        @type boot_index: String
        @param volume_size: Volume Size in GB
        @type volume_size: Int
        @param source_type: snap or blank, from where the volume was created
        @type source_type: String
        @param destination_type: The type of the target virtual device
        @type destination_type: String
        @return: The Block Device Mapping
        @rtype: List of dicts
        """

        # Creating block device
        block_device_matrix = [{
            "boot_index": boot_index,
            "uuid": uuid,
            "volume_size": volume_size,
            "source_type": source_type,
            "destination_type": destination_type,
            "delete_on_termination": delete_on_termination}]
        return block_device_matrix

    def create_block_device_mapping_v2_virt3099(self, boot_index, uuid,
                                       source_type,
                                       delete_on_termination):
        """
        @summary: Creates Block Device on the fly
        @param uuid: The uuid of the volume
        @type uuid: String
        @param delete_on_termination:  True or False also 0 or 1
        @type delete_on_termination: Boolean
        @param boot_index: Used to order the boot disks
        @type boot_index: String
        @param volume_size: Volume Size in GB
        @type volume_size: Int
        @param source_type: snap or blank, from where the volume was created
        @type source_type: String
        @param destination_type: The type of the target virtual device
        @type destination_type: String
        @return: The Block Device Mapping
        @rtype: List of dicts
        """

        # Creating block device
        block_device_matrix = [{
            "boot_index": boot_index,
            "uuid": uuid,
            "source_type": source_type,
            "delete_on_termination": delete_on_termination}]
        return block_device_matrix
