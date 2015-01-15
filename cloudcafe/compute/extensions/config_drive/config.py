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
    def vendor_meta_filepath(self):
        """Path to the Vendor Config Drive metadata"""
        return self.get("vendor_meta_path")

    @property
    def base_path_to_mount(self):
        """Path to the desired location to mount"""
        return self.get("base_path_to_mount")

    @property
    def mount_source_path(self):
        """Path to the config drive source"""
        return self.get("mount_source_path")

    @property
    def min_size(self):
        """Projected minimun size of config drive"""
        return int(self.get("min_size"))

    @property
    def max_size(self):
        """Projected maximum size of config drive"""
        return int(self.get("max_size"))


class CloudInitConfig(ConfigSectionInterface):

    SECTION_NAME = 'cloud_init'

    @property
    def user_data_script(self):
        """Path to the user data script"""
        return self.get("user_data_script")

    @property
    def include_script(self):
        """Path to the include format data script"""
        return self.get("include_script")

    @property
    def boothook_script(self):
        """Path to the boothook format data script"""
        return self.get("boothook_script")

    @property
    def part_handler_script(self):
        """Path to the part handler format data script"""
        return self.get("part_handler_script")

    @property
    def mime_gzip_script(self):
        """Path to the mime gzip format data script"""
        return self.get("mime_gzip_script")

    @property
    def upstart_script(self):
        """Path to the upstart format data script"""
        return self.get("upstart_script")

    @property
    def cloud_init_directory(self):
        """Main Cloud Init Dorectory"""
        return self.get("cloud_init_directory")

    @property
    def cloud_config_format_script(self):
        """Path to the cloud config script"""
        return self.get("cloud_config_format_script")

    @property
    def user_data_created_directory(self):
        """Directory that is created by the script"""
        return self.get("user_data_created_directory")
