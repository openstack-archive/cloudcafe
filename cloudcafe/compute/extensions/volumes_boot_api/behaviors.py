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

from cloudcafe.compute.common.behaviors import BaseComputeBehavior
from cloudcafe.compute.common.types import NovaServerStatusTypes \
    as ServerStates
from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.compute.common.exceptions import \
    TimeoutException, BuildErrorException, RequiredResourceException


class VolumeServerBehaviors(BaseComputeBehavior):

    def __init__(self, servers_client, images_client, servers_config,
                 images_config, flavors_config, server_behaviors,
                 boot_from_volume_client=None, security_groups_config=None):
        super(VolumeServerBehaviors, self).__init__()
        self.config = servers_config
        self.servers_client = servers_client
        self.images_client = images_client
        self.images_config = images_config
        self.flavors_config = flavors_config
        self.server_behaviors = server_behaviors
        self.boot_from_volume_client = boot_from_volume_client
        self.security_groups_config = security_groups_config

    def create_active_server(
            self, name=None, image_ref=None, flavor_ref=None,
            personality=None, user_data=None, metadata=None,
            accessIPv4=None, accessIPv6=None, disk_config=None,
            networks=None, key_name=None, config_drive=None,
            scheduler_hints=None, admin_pass=None, max_count=None,
            min_count=None, block_device_mapping=None, block_device=None,
            security_groups=None):
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
        """

        if name is None:
            name = rand_name('testserver')
        if ((image_ref is None) and (block_device_mapping is None) and (
                block_device is None)):
                    image_ref = self.images_config.primary_image
        if flavor_ref is None:
            flavor_ref = self.flavors_config.primary_flavor
        if self.config.default_network:
            networks = [{'uuid': self.config.default_network}]

        default_groups = None
        if (self.security_groups_config
                and self.security_groups_config.default_security_group):
            default_groups = [
                {"name": self.security_groups_config.default_security_group}]

        if default_groups and security_groups:
            security_groups.extend(default_groups)
        else:
            security_groups = security_groups or default_groups

        failures = []
        attempts = self.config.resource_build_attempts
        for attempt in range(attempts):

            self._log.debug('Attempt {attempt} of {attempts} '
                            'to create server.'.format(attempt=attempt + 1,
                                                       attempts=attempts))

            resp = self.boot_from_volume_client.create_server(
                name, flavor_ref, block_device_mapping_v2=block_device,
                max_count=max_count, min_count=min_count,
                networks=networks, image_ref=image_ref,
                personality=personality, user_data=user_data,
                metadata=metadata, accessIPv4=accessIPv4,
                accessIPv6=accessIPv6, disk_config=disk_config,
                admin_pass=admin_pass, key_name=key_name,
                config_drive=config_drive, scheduler_hints=scheduler_hints,
                security_groups=security_groups)
            server_obj = resp.entity
            create_request_id = resp.headers.get('x-compute-request-id')

            try:
                resp = self.server_behaviors.wait_for_server_status(
                    server_obj.id, ServerStates.ACTIVE)
                # Add the password from the create request
                # into the final response
                resp.entity.admin_pass = server_obj.admin_pass
                resp.headers['x-compute-request-id'] = create_request_id
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
