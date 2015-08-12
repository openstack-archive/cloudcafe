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

from warnings import warn

from cloudcafe.common.models.configuration import ConfigSectionInterface


class FlavorsConfig(ConfigSectionInterface):

    SECTION_NAME = 'flavors'

    @property
    def primary_flavor(self):
        """Default flavor to be used when building servers in compute test"""
        return self.get("primary_flavor")

    @property
    def secondary_flavor(self):
        """Alternate flavor to be used in compute test"""
        return self.get("secondary_flavor")

    @property
    def resize_enabled(self):
        """Deprecated. Determines if resize is enabled for this flavor class"""
        warn(
            "This config property is deprecated. Please use the config "
            "property 'resize_up_enabled' or the"
            " 'resize_down_enabled' instead.")
        return self.get_boolean("resize_enabled")

    @property
    def resize_up_enabled(self):
        """Determines if resize up is enabled for this flavor class"""
        return self.get_boolean("resize_up_enabled")

    @property
    def resize_down_enabled(self):
        """Determines if resize down is enabled for this flavor class"""
        return self.get_boolean("resize_down_enabled")
