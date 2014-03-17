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

from cloudcafe.common.models.configuration import ConfigSectionInterface


class ServersConfig(ConfigSectionInterface):

    SECTION_NAME = 'servers'

    @property
    def resource_build_attempts(self):
        """
        Number of times to try to build a resource when using a behavior.
        """
        return int(self.get("resource_build_attempts", 1))

    @property
    def instance_auth_strategy(self):
        """Strategy to use for authenticating to an instance (password|key)"""
        return self.get("instance_auth_strategy")

    @property
    def split_ephemeral_disk_enabled(self):
        """
        Enable if splitting of ephemeral disks (limiting of the disk
        size and splitting into multiple disks if necessary) is enabled.
        """
        return self.get_boolean("split_ephemeral_disk_enabled", False)

    @property
    def ephemeral_disk_max_size(self):
        """
        If ephemeral disk splitting is enabled, this is the maximum
        size of an ephemeral disk. If this value is less than the
        requested ephemeral disk, multiple disks will be created.
        """
        return int(self.get("ephemeral_disk_max_size", 0))

    @property
    def disk_config_override(self):
        """Optional override for the disk_config parameter (all actions)"""
        return self.get("disk_config_override")

    @property
    def disk_format_type(self):
        """Format type to be used when formatting an instance's disk"""
        return self.get("disk_format_type")

    @property
    def server_status_interval(self):
        """Amount of time to wait between polling the status of a server"""
        return int(self.get("server_status_interval"))

    @property
    def server_build_timeout(self):
        """
        Length of time to wait before timing out on a server reaching
        the ACTIVE state
        """
        return int(self.get("server_build_timeout"))

    @property
    def server_boot_timeout(self):
        """
        Length of time to wait before timing out on a server boot
        """
        return int(self.get("server_boot_timeout"))

    @property
    def server_resize_timeout(self):
        """
        Length of time to wait before timing out on a server reaching
        the VERIFY_RESIZE state
        """
        return int(self.get("server_resize_timeout"))

    @property
    def network_for_ssh(self):
        """
        Name of network to be used for remote connections
        (ie. public, private)
        """
        return self.get("network_for_ssh")

    @property
    def ip_address_version_for_ssh(self):
        """
        IP address version to be used for remote connections
        (ie. 4, 6)
        """
        return int(self.get("ip_address_version_for_ssh"))

    @property
    def instance_disk_path(self):
        """Primary disk path of instances under test"""
        return self.get("instance_disk_path")

    @property
    def connection_retry_interval(self):
        """
        Amount of time to wait between connection attempts
        """
        return int(self.get("connection_retry_interval"))

    @property
    def connection_timeout(self):
        """
        Amount of time to wait before giving up on connecting to an instance
        """
        return int(self.get("connection_timeout"))

    @property
    def expected_networks(self):
        """
        Dictionary containing the expected networks and the IP address types
        expected to be assigned per network.
        """
        return eval(self.get("expected_networks"))

    @property
    def default_network(self):
        """Id of the network to use by default for servers"""
        return self.get("default_network")

    @property
    def personality_file_injection_enabled(self):
        """If personality files can be injected for this deployment"""
        return self.get_boolean("personality_file_injection_enabled", True)

class BlockDeviceMappingConfig(ConfigSectionInterface):

    SECTION_NAME = 'block_device_mapping'

    @property
    def bdm_devname(self):
        """device name"""
        return self.get("bdm_devname")

    @property
    def bdm_type(self):
        """server type"""
        return self.get("bdm_type")

    @property
    def bdm_size(self):
        """size in gb"""
        return int(self.get("bdm_size"))

    @property
    def bdm_delete_on_termination(self):
        """delete volume on termination"""
        return self.get("bdm_delete_on_termination")
