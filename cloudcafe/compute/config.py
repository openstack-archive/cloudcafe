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

class ComputeConfig(ConfigSectionInterface):

    SECTION_NAME = 'compute'

    @property
    def hypervisor(self):
        return self.get("hypervisor")


class ComputeEndpointConfig(ConfigSectionInterface):

    SECTION_NAME = 'compute_endpoint'

    @property
    def region(self):
        return self.get("region")

    @property
    def compute_endpoint_name(self):
        return self.get("compute_endpoint_name")


class ComputeAdminEndpointConfig(ComputeEndpointConfig):

    SECTION_NAME = 'compute_admin_endpoint'
