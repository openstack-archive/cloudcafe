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


class VolumesAPIConfig(ConfigSectionInterface):
    SECTION_NAME = 'volumes_api_v1'

    @property
    def serialize_format(self):
        return self.get("serialize_format", default="json")

    @property
    def deserialize_format(self):
        return self.get("deserialize_format", default="json")

#Volumes behavior config
    @property
    def default_volume_type(self):
        return self.get("default_volume_type", default=None)

    @property
    def max_volume_size(self):
        return self.get("max_volume_size", default=None)

    @property
    def min_volume_size(self):
        return self.get("min_volume_size", default=None)

    @property
    def volume_status_poll_frequency(self):
        return self.get("volume_status_poll_frequency", default=None)

    @property
    def volume_create_max_timeout(self):
        return self.get("volume_create_timeout", default=None)

    @property
    def volume_delete_min_timeout(self):
        return self.get("volume_delete_min_timeout", default=None)

    @property
    def volume_delete_max_timeout(self):
        return self.get("volume_delete_max_timeout", default=None)

    @property
    def volume_delete_wait_per_gigabyte(self):
        return self.get("volume_delete_wait_per_gigabyte", default=None)

#Snapshot behaviors config
    @property
    def snapshot_status_poll_frequency(self):
        return self.get("snapshot_status_poll_frequency", default=None)

    @property
    def snapshot_create_max_timeout(self):
        return self.get("snapshot_create_max_timeout", default=None)

    @property
    def snapshot_create_min_timeout(self):
        """Absolute lower limit on calculated snapshot create timeouts"""
        return self.get("snapshot_create_min_timeout", default=None)

    @property
    def snapshot_create_base_timeout(self):
        """Amount of time added by default to calculated snapshot create
        timeouts"""
        return self.get("snapshot_create_min_timeout", default=0)

    @property
    def snapshot_create_wait_per_gigabyte(self):
        return self.get("snapshot_create_wait_per_gigabyte", default=None)

    @property
    def snapshot_delete_max_timeout(self):
        """Absolute upper limit on calculated snapshot delete timeouts"""
        return self.get("snapshot_delete_max_timeout", default=None)

    @property
    def snapshot_delete_min_timeout(self):
        """Absolute lower limit on calculated snapshot delete timeouts
        """
        return self.get("snapshot_delete_min_timeout", default=None)

    @property
    def snapshot_delete_wait_per_gigabyte(self):
        """If set, volume snapshot delete behaviors can estimate the time
        it will take a particular volume to delete given it's size"""
        return self.get("snapshot_delete_wait_per_gigabyte", default=None)
