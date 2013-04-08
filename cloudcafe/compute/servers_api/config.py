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
        return self.get("ip_address_version_for_ssh")

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
