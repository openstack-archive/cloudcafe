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


class ConfigDriveConfig(ConfigSectionInterface):

    SECTION_NAME = 'config_drive'

    @property
    def openstack_meta_filepath(self):
        """Path to the Openstack Config Drive metadata"""
        return self.get("openstack_meta_path")

    @property
    def ec_meta_filepath(self):
        """Path to the EC2 Config Drive metadata"""
        return self.get("ec_meta_path")

    @property
    def base_path_to_mount(self):
        """Path to the desired location to mount"""
        return self.get("base_path_to_mount")

    @property
    def mount_source_path(self):
        """Path to the config drive source"""
        return self.get("mount_source_path")
