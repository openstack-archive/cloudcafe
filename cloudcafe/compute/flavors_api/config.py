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


class FlavorsConfig(ConfigSectionInterface):

    SECTION_NAME = 'flavors'

    @property
    def primary_flavor(self):
        """Default flavor to be used when building servers in compute tests"""
        return self.get("primary_flavor")

    @property
    def secondary_flavor(self):
        """Alternate flavor to be used in compute tests"""
        return self.get("secondary_flavor")
