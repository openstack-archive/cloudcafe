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

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.compute.extensions.config_drive.models.cd_openstack_meta import \
    OpenStackMeta
from cloudcafe.compute.extensions.config_drive.models.cd_ec_meta import \
    EcMeta


class ConfigDriveBehaviors(BaseBehavior):

    def __init__(self, servers_client, servers_config,
                 server_behaviors):

        self.config = servers_config
        self.servers_client = servers_client
        self.server_behaviors = server_behaviors

    def get_openstack_metadata(self, server, servers_config, key,
                               filepath):
        """
        @summary:Returns openstack metadata on config drive
        @return: Response Object containing openstack meta domain object
        @rtype: Request Response Object
        """

        remote_client = self.server_behaviors.get_remote_instance_client(
            server, servers_config, key=key)
        openstack_meta_str = remote_client.get_file_details(
            filepath=filepath)
        return OpenStackMeta.deserialize(openstack_meta_str.content, 'json')

    def get_ec_metadata(self, server, servers_config, key,
                        filepath):
        """
        @summary:Returns ec2 metadata on config drive
        @return: Response Object containing ec2 meta domain object
        @rtype: Request Response Object
        """

        remote_client = self.server_behaviors.get_remote_instance_client(
            server, servers_config, key=key)
        ec_meta_str = remote_client.get_file_details(
            filepath=filepath)
        return EcMeta.deserialize(ec_meta_str.content, 'json')

    def create_dir_and_mount_config_drive(self, server, servers_config, key,
                                          source_path, destination_path):
        """
        @summary:Returns already mounted config drive
        @return: Silent
        @rtype: None
        """
        remote_client = self.server_behaviors.get_remote_instance_client(
            self.server, self.servers_config, key=self.key.private_key)
        remote_client.create_directory(
            path=self.config_drive_config.base_path_to_mount)
        remote_client.mount_file_to_destination_directory(
            source_path=source_path,
            destination_path=destination_path)
