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

from cloudcafe.networking.networks.common.config import NetworkingBaseConfig


class NetworksConfig(NetworkingBaseConfig):
    """Network is the resource"""

    SECTION_NAME = 'networks'

    @property
    def public_network_id(self):
        """The uuid of the public network"""
        return self.get("public_network_id",
                        "00000000-0000-0000-0000-000000000000")

    @property
    def service_network_id(self):
        """The uuid of the service network (aka private)"""
        return self.get("service_network_id",
                        "11111111-1111-1111-1111-111111111111")

    @property
    def resource_build_attempts(self):
        """Number of times to try to create a resource"""
        return int(self.get("resource_build_attempts", 1))

    @property
    def resource_update_attempts(self):
        """Number of times to try to update a resource"""
        return int(self.get("resource_update_attempts", 1))

    @property
    def resource_get_attempts(self):
        """Number of times to try to get a resource"""
        return int(self.get("resource_get_attempts", 1))

    @property
    def resource_list_attempts(self):
        """Number of times to try to list a resource"""
        return int(self.get("resource_list_attempts", 1))

    @property
    def resource_delete_attempts(self):
        """Number of times to try to delete a resource"""
        return int(self.get("resource_delete_attempts", 1))

    @property
    def keep_resources(self):
        """Flag for not deleting resources on tearDown"""
        return self.get_boolean("keep_resources", False)

    @property
    def keep_resources_on_failure(self):
        """Flag for not deleting resources w failures on tearDown"""
        return self.get_boolean("keep_resources_on_failure", False)

    @property
    def resource_create_timeout(self):
        """Seconds to wait for creating a resource"""
        return int(self.get("resource_create_timeout", 15))

    @property
    def resource_delete_timeout(self):
        """Seconds to wait for deleting a resource"""
        return int(self.get("resource_delete_timeout", 15))

    @property
    def starts_with_name(self):
        """Network start name label for test runs"""
        return self.get("starts_with_name", "test_net")
