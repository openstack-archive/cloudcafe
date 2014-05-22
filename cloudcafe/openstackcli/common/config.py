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


class OpenstackCLI_CommonConfig(ConfigSectionInterface):

    SECTION_NAME = 'openstack_cli_common'

    @property
    def debug(self):
        """Running the openstack cli with debug on by default gives much more
           useful output in the logs"""
        return self.get_boolean('debug', default=True)

    @property
    def retries(self):
        return self.get('retries')

    @property
    def os_username(self):
        return self.get('os_username')

    @property
    def os_password(self):
        return self.get('os_password')

    @property
    def os_tenant_name(self):
        return self.get('os_tenant_name')

    @property
    def os_auth_url(self):
        return self.get('os_auth_url')

    @property
    def os_region_name(self):
        return self.get('os_region_name')

    @property
    def os_cacert(self):
        return self.get('os_cacert')
