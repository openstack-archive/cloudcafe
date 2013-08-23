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

from cloudcafe.compute.extensions.config_drive.models.cd_openstack_meta import \
    OpenStackMeta
from cloudcafe.compute.servers_api.behaviors import ServerBehaviors


class ConfigDriveBehaviors(ServerBehaviors):

    def get_openstack_metadata(self, server, servers_config, key):
        """
        @summary:Returns openstack metadata on config drive
        @return: Response Object containing openstack meta domain object
        @rtype: Request Response Object
        """

        remote_client = self.get_remote_instance_client(
            server, servers_config, key=key)
        openstack_meta_str = remote_client.get_file_details(
            filepath='/mnt/config/openstack/latest/meta_data.json')
        return OpenStackMeta.deserialize(openstack_meta_str.content, 'json')
