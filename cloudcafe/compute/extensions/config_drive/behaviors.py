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

from cloudcafe.compute.common.behaviors import BaseComputeBehavior
from cloudcafe.compute.extensions.config_drive.models.\
    config_drive_openstack_meta import OpenStackMeta
from cloudcafe.compute.extensions.config_drive.models.\
    config_drive_vendor_meta import VendorMetadata
from cloudcafe.compute.extensions.config_drive.models.\
    config_drive_ec_metadata import EcMetadata


class ConfigDriveBehaviors(BaseComputeBehavior):

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
            file_path=filepath)
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
            file_path=filepath)
        return EcMetadata.deserialize(ec_meta_str.content, 'json')

    def get_vendor_metadata(self, server, servers_config, key,
                            filepath):
        """
        @summary:Returns vendor metadata on config drive
        @return: Response Object containing vendor meta domain object
        @rtype: Request Response Object
        """

        remote_client = self.server_behaviors.get_remote_instance_client(
            server, servers_config, key=key)
        vendor_meta_str = remote_client.get_file_details(
            file_path=filepath)
        return VendorMetadata.deserialize(vendor_meta_str.content, 'json')

    def mount_config_drive(self, server, servers_config, key,
                           source_path, destination_path):
        """
        @summary: Mounts config drive
        @return: Silent
        @rtype: None
        """
        remote_client = self.server_behaviors.get_remote_instance_client(
            server, servers_config, key=key)
        remote_client.create_directory(
            path=destination_path)
        remote_client.mount_disk(
            source_path=source_path,
            destination_path=destination_path)

    def read_cloud_init_for_config_drive(self, file_path):
        """
        @summary:Returns the Cloud Init script as string
        @return: string for user data processing
        @rtype: String
        """
        with open(file_path, "r") as myfile:
            data = myfile.read()
        return data

    def status_of_manage_etc_hosts(self, server, servers_config, key):
        """
        @summary:Returns the status of managed etc hosts
        @return: Boolean status of managed etc hosts
        @rtype: Boolean
        """
        remote_client = self.server_behaviors.get_remote_instance_client(
            server, servers_config, key=key)
        str = remote_client.get_file_details('/etc/hosts').content
        if "'manage_etc_hosts' as True" in str:
            dir_cloud_config_present = True
        else:
            dir_cloud_config_present = False
        return dir_cloud_config_present

    def get_config_drive_details(self, file_path, base_path_to_mount, server,
                                 server_config, private_key, filepath):
        """
        @summary:Returns user data, directory size and metadata
        @return: user data, directory details and metadata
        @rtype: String
        """

        remote_client = self.server_behaviors.get_remote_instance_client(
            server, server_config, key=private_key)
        self.user_data = remote_client.get_file_details(
            file_path=file_path).content
        self.kb_size = remote_client.get_directory_details(base_path_to_mount)
        self.openstack_meta = remote_client.get_file_details(
            file_path=filepath)
        return_values = (
            self.user_data, self.kb_size,
            OpenStackMeta.deserialize(self.openstack_meta.content, 'json'))
        return return_values
