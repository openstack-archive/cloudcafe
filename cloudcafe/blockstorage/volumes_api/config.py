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

from cafe.engine.models.configuration import BaseConfigSectionInterface


class VolumesAPIConfig(BaseConfigSectionInterface):
    SECTION_NAME = 'volumes_api'

    @property
    def serialize_format(self):
        return self.get("serialize_format")

    @property
    def deserialize_format(self):
        return self.get("deserialize_format")

    @property
    def max_volume_size(self):
        return self.get("max_volume_size", default='1024')

    @property
    def min_volume_size(self):
        return self.get("min_volume_size", default='1')

    @property
    def volume_create_timeout(self):
        return self.get("volume_create_timeout", default='10')

    @property
    def volume_status_poll_frequency(self):
        return self.get("volume_status_poll_frequency", default='30')

    @property
    def volume_delete_wait_per_gig(self):
        return self.get("volume_delete_wait_per_gig", default='30')

    @property
    def snapshot_create_timeout(self):
        return self.get("snapshot_create_timeout", default='10')

    @property
    def snapshot_status_poll_frequency(self):
        return self.get("snapshot_status_poll_frequency", default='30')

    @property
    def volume_snapshot_delete_min_timeout(self):
        """Absolute lower limit on calculated volume snapshot delete timeouts
        """
        return self.get("volume_delete_wait_per_gig", default=None)

    @property
    def volume_snapshot_delete_max_timeout(self):
        """Absolute upper limit on calculated volume snapshot delete timeouts
        """
        return self.get("volume_delete_wait_per_gig", default=None)

    @property
    def volume_snapshot_delete_wait_per_gig(self):
        """If set, volume snapshot delete behaviors can estimate the time
        it will take a particular volume to delete given it's size"""
        return self.get("volume_delete_wait_per_gig", default=None)
