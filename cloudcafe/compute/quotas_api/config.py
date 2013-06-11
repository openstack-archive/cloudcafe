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


class DefaultQuotaSetConfig(ConfigSectionInterface):

    SECTION_NAME = 'default-quota-set'

    @property
    def metadata_items(self):
        """Default metadata items"""
        return int(self.get('metadata_items'))

    @property
    def injected_file_content_bytes(self):
        """Default size of injected file content in bytes"""
        return int(self.get('injected_file_content_bytes'))

    @property
    def ram(self):
        """Default ram size"""
        return int(self.get("ram"))

    @property
    def floating_ips(self):
        """Default number of floating ips"""
        return self.get('floating_ips')

    @property
    def key_pairs(self):
        """Default number of key pairs"""
        return self.get('key_pairs')

    @property
    def instances(self):
        """Default number of instances"""
        return self.get('instances')

    @property
    def security_group_rules(self):
        """Default number of security group rules"""
        return int(self.get('security_group_rules'))

    @property
    def injected_files(self):
        """Default number of injected files"""
        return int(self.get('injected_files'))

    @property
    def cores(self):
        """Default number of Cores"""
        return int(self.get('cores'))

    @property
    def injected_file_path_bytes(self):
        """Default injected file path in bytes"""
        return int(self.get('injected_file_path_bytes'))

    @property
    def security_groups(self):
        """Default number of security groups"""
        return int(self.get('security_group_rules'))
