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
        """Sets all reqeusts made to this api in either json or xml"""
        return self.get("serialize_format", default="json")

    @property
    def deserialize_format(self):
        """Requests all responses from this api to be in either json or xml"""
        return self.get("deserialize_format", default="json")

    @property
    def version_under_test(self):
        """Version of the cinder api under test, either '1'  or '2' """
        return self.get("version_under_test", default="1")

# Volumes behavior config
    @property
    def default_volume_type(self):
        """Sets the default volume type for some behaviors and tests"""
        return self.get("default_volume_type")

    @property
    def max_volume_size(self):
        """Maximum volume size allowed by the environment under test"""
        return int(self.get("max_volume_size", default=1024))

    @property
    def min_volume_size(self):
        """Minimum volume size allowed by the environment under test"""
        return int(self.get("min_volume_size", default=1))

    @property
    def volume_status_poll_frequency(self):
        """Controlls the rate at which some behaviors will poll the cinder
        api for information.
        """
        return int(self.get("volume_status_poll_frequency", default=5))

    @property
    def volume_create_min_timeout(self):
        """Minimum time to allow any behavior to wait for a volume to finish
        creating
        """
        return int(self.get("volume_create_min_timeout", default=1))

    @property
    def volume_create_max_timeout(self):
        """Maximum time to allow any behavior to wait for a volume to finish
        creating
        """
        return int(self.get("volume_create_max_timeout", default=600))

    @property
    def volume_create_wait_per_gigabyte(self):
        """Used by some behaviors to attempt to calculate the time it will
        take for a volume to be created based on its size
        """
        return int(self.get("volume_create_wait_per_gigabyte", default=1))

    @property
    def volume_create_base_timeout(self):
        """Amount of time added by default to the final calculated volume
        create timeouts for some behaviors.  Useful for adding a constant
        amount of time to create timeouts globaly for dialing in good test
        timeouts
        """
        return int(self.get("volume_create_base_timeout", default=0))

    @property
    def volume_clone_min_timeout(self):
        """Minimum time to allow any behavior to wait for a volume to finish
        creating when using another volume as its source.
        """
        return int(self.get("volume_clone_min_timeout", default=2))

    @property
    def volume_clone_max_timeout(self):
        """Maximum time to allow any behavior to wait for a volume to finish
        creating when using another volume as its source.
        """
        return int(self.get("volume_clone_max_timeout", default=1200))

    @property
    def volume_clone_wait_per_gigabyte(self):
        """Used by some behaviors to attempt to calculate the time it will
        take for a volume to be created based on it's size when using another
        volume as its source
        """
        return int(self.get("volume_clone_wait_per_gigabyte", default=2))

    @property
    def volume_clone_base_timeout(self):
        """Amount of time added by default to the final calculated volume
        clone timeouts for some behaviors.  Useful for adding a constant
        amount of time to clone timeouts globaly for dialing in good test
        timeouts.
        """
        return int(self.get("volume_create_base_timeout", default=0))

    @property
    def volume_delete_min_timeout(self):
        """Maximum time some behaviors wait for a volume to be confirmed
        deleted before raising an error"""
        return int(self.get("volume_delete_min_timeout", default=1))

    @property
    def volume_delete_max_timeout(self):
        """Maximum time some behaviors wait for a volume to be confirmed
        deleted before raising an error"""
        return int(self.get("volume_delete_max_timeout", default=3600))

    @property
    def volume_delete_wait_per_gigabyte(self):
        """Used by some behaviors to attempt to calculate the time it will
        take for a volume to be deleted based on it's size
        """
        return int(self.get("volume_delete_wait_per_gigabyte", default=1))

# Snapshot behaviors config
    @property
    def snapshot_status_poll_frequency(self):
        """Controlls the rate at which some behaviors will poll the cinder
        api for information.
        """
        return int(self.get("snapshot_status_poll_frequency", default=10))

    @property
    def snapshot_create_max_timeout(self):
        """Maximum time to allow any behavior to wait for a snapshot to finish
        creating
        """
        return int(self.get("snapshot_create_max_timeout", default=36000))

    @property
    def snapshot_create_min_timeout(self):
        """Minimum time to allow any behavior to wait for a snapshot to finish
        creating
        """
        return int(self.get("snapshot_create_min_timeout", default=10))

    @property
    def snapshot_create_base_timeout(self):
        """Amount of time added by default to the final calculated volume
        snapshot timeouts for some behaviors.  Useful for adding a constant
        amount of time to volume snapshot timeouts globaly for dialing in good
        test timeouts.
        """
        return int(self.get("snapshot_create_base_timeout", default=0))

    @property
    def snapshot_create_wait_per_gigabyte(self):
        """Used by some behaviors to attempt to calculate the time it will
        take for a snapshot to be created based on the size of the original
        volume
        """
        return int(self.get("snapshot_create_wait_per_gigabyte", default=600))

    @property
    def snapshot_delete_max_timeout(self):
        """Maximum time some behaviors wait for a volume snapshot to be
        confirmed deleted before raising an error
        """
        return int(self.get("snapshot_delete_max_timeout", default=600))

    @property
    def snapshot_delete_min_timeout(self):
        """Minimum time some behaviors wait for a volume snapshot to be
        confirmed deleted before raising an error
        """
        return int(self.get("snapshot_delete_min_timeout", default=60))

    @property
    def snapshot_delete_wait_per_gigabyte(self):
        """Used by some behaviors to attempt to calculate the time it will
        take for a snapshot to be deleted based on the size of the original
        volume.
        """
        return int(self.get("snapshot_delete_wait_per_gigabyte", default=60))

    @property
    def snapshot_delete_base_timeout(self):
        """Amount of time added by default to the final calculated volume
        snapshot timeouts for some behaviors.  Useful for adding a constant
        amount of time to volume snapshot timeouts globaly for dialing in good
        test timeouts.
        """
        return int(self.get("snapshot_delete_base_timeout", default=60))

# Misc
    @property
    def min_volume_from_image_size(self):
        """Minimum size a volume can be if building from an image.
        Used by some behaviors and tests.  Depending on how the environment
        under test is deployed, this value may be superceded by the
        minimum allowed volume size"""
        return int(self.get("min_volume_from_image_size", default=1))

    @property
    def image_filter(self):
        """Expects Json.  Returns an empty dictionary by default (no filter).
        Dictionary keys should be attributes of the image model, and key values
        should be a list of values for that model attribute.
        Used by some tests to decide which images to target for a given
        test run.
        """
        return json.loads(self.get('image_filter', '{}'))

    @property
    def volume_type_filter(self):
        """Expects Json.  Returns an empty dictionary by default.
        Dictionary keys should be attributes of the volume type model, and
        key values should be a list of values for that model attribute.
        Used by some tests to decide which images to target for a given
        test run.
        """
        return json.loads(self.get('volume_type_filter', '{}'))
