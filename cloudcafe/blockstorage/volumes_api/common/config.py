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

import json
from cloudcafe.common.models.configuration import ConfigSectionInterface


class VolumesAPIConfig(ConfigSectionInterface):
    SECTION_NAME = 'volumes_api'

    @property
    def serialize_format(self):
        return self.get("serialize_format", default="json")

    @property
    def deserialize_format(self):
        return self.get("deserialize_format", default="json")

    @property
    def version_under_test(self):
        return self.get("version_under_test", default="1")

# Volumes behavior config
    @property
    def default_volume_type(self):
        return self.get("default_volume_type")

    @property
    def max_volume_size(self):
        return int(self.get("max_volume_size", default=1024))

    @property
    def min_volume_size(self):
        return int(self.get("min_volume_size", default=1))

    @property
    def volume_status_poll_frequency(self):
        return int(self.get("volume_status_poll_frequency", default=5))

    @property
    def volume_create_min_timeout(self):
        return int(self.get("volume_create_min_timeout", default=1))

    @property
    def volume_create_max_timeout(self):
        return int(self.get("volume_create_max_timeout", default=600))

    @property
    def volume_create_wait_per_gigabyte(self):
        return int(self.get("volume_create_wait_per_gigabyte", default=1))

    @property
    def volume_create_base_timeout(self):
        """Amount of time added by default to the final calculated volume
        create timeouts.
        """
        return int(self.get("volume_create_base_timeout", default=0))

    @property
    def volume_delete_min_timeout(self):
        return int(self.get("volume_delete_min_timeout", default=1))

    @property
    def volume_delete_max_timeout(self):
        return int(self.get("volume_delete_max_timeout", default=3600))

    @property
    def volume_delete_wait_per_gigabyte(self):
        return int(self.get("volume_delete_wait_per_gigabyte", default=1))

# Snapshot behaviors config
    @property
    def snapshot_status_poll_frequency(self):
        return int(self.get("snapshot_status_poll_frequency", default=10))

    @property
    def snapshot_create_max_timeout(self):
        return int(self.get("snapshot_create_max_timeout", default=36000))

    @property
    def snapshot_create_min_timeout(self):
        """Absolute lower limit on calculated snapshot create timeouts"""

        return int(self.get("snapshot_create_min_timeout", default=10))

    @property
    def snapshot_create_base_timeout(self):
        """Amount of time added by default to the final calculated snapshot
        create timeouts.
        """
        return int(self.get("snapshot_create_base_timeout", default=0))

    @property
    def snapshot_create_wait_per_gigabyte(self):
        return int(self.get("snapshot_create_wait_per_gigabyte", default=600))

    @property
    def snapshot_delete_max_timeout(self):
        """Absolute upper limit on calculated snapshot delete timeouts"""
        return int(self.get("snapshot_delete_max_timeout", default=36000))

    @property
    def snapshot_delete_min_timeout(self):
        """Absolute lower limit on calculated snapshot delete timeouts"""
        return int(self.get("snapshot_delete_min_timeout", default=0))

    @property
    def snapshot_delete_wait_per_gigabyte(self):
        """If set, volume snapshot delete behaviors can estimate the time
        it will take a particular volume to delete given it's size
        """
        return int(self.get("snapshot_delete_wait_per_gigabyte", default=60))

# Misc
    @property
    def min_volume_from_image_size(self):
        """Limit the smallest size a volume can be if building from an image"""
        return int(self.get("min_volume_from_image_size", default=1))

    @property
    def image_filter(self):
        """Expects Json.  Returns an empty dictionary by default.
        Dictionary keys should be attributes of the image model, and key values
        should be a list of values for that model attribute.
        """
        return json.loads(self.get('image_filter', '{}'))

    @property
    def volume_type_filter(self):
        """Expects Json.  Returns an empty dictionary by default.
        Dictionary keys should be attributes of the volume type model, and
        key values should be a list of values for that model attribute.
        """
        return json.loads(self.get('volume_type_filter', '{}'))
