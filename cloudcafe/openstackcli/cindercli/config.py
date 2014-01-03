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

from ast import literal_eval
from cloudcafe.common.models.configuration import ConfigSectionInterface


class CinderCLI_Config(ConfigSectionInterface):

    SECTION_NAME = 'cinder_cli'

    @property
    def service_type(self):
        return self.get('service_type')

    @property
    def service_name(self):
        return self.get('service_name')

    @property
    def volume_service_name(self):
        return self.get('volume_service_name')

    @property
    def endpoint_type(self):
        return self.get('endpoint_type')

    @property
    def os_volume_api_version(self):
        return self.get('os_volume_api_version')

    @property
    def environment_variable_dictionary(self):
        """Expects a python dictionary as a string.  Returns an empty dict
        by default.
        """
        return literal_eval(self.get('environment_variable_dictionary', '{}'))
