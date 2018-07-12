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
from warnings import warn

from cloudcafe.common.models.configuration import ConfigSectionInterface


class VolumesAPIConfig(ConfigSectionInterface):
    SECTION_NAME = 'volumes_api'

    @property
    def serialize_format(self):
        """Sets all reqeusts made to the volumes api in either json or xml"""
        return self.get("serialize_format", default="json")

    @property
    def deserialize_format(self):
        """Requests all responses from the volumes api to be in either json or
        xml
        """
        return self.get("deserialize_format", default="json")

    @property
    def version_under_test(self):
        """Version of the cinder api under test, either '1'  or '2' """
        return self.get("version_under_test", default="1")

    @property
    def volume_status_poll_frequency(self):
        """Controls the rate at which some behaviors will poll the cinder
        api for volume information.
        """
        return int(self.get("volume_status_poll_frequency", default=5))

    @property
    def snapshot_status_poll_frequency(self):
        """Controls the rate at which some behaviors will poll the cinder
        api for snapshot information.
        """
        return int(self.get("snapshot_status_poll_frequency", default=10))

    @property
    def volume_status_poll_failure_max_retries(self):
        """Controls the number of times the status progression verifier will
        allow calls to the Volumes API for status updates to fail
        """
        return int(
            self.get("volume_status_poll_failure_max_retries", default=3))

    @property
    def snapshot_status_poll_failure_max_retries(self):
        """Controls the number of times the status progression verifier will
        allow calls to the Volume Snapshots API for status updates to fail
        """
        return int(
            self.get("snapshot_status_poll_failure_max_retries", default=3))

# Volume Type configuration
    @property
    def volume_type_properties(self):
        """Dictionary of volume type properties"""
        data = self.get(
            'volume_type_properties',
            '[{"name":null, "id":null, "min_size":null, "max_size":null}]')
        return json.loads(data)

    @property
    def default_volume_type(self):
        """Sets the default volume type for some non-data-driven tests."""
        return self.get("default_volume_type")

    @property
    def default_volume_type_min_size(self):
        """The minimum size allowed by the API for the configured
        default volume type
        """
        return int(self.get("default_volume_type_min_size"))

    @property
    def default_volume_type_max_size(self):
        """The maximum size allowed by the API for the configured
        default volume type
        """
        return int(self.get("default_volume_type_max_size"))

    @property
    def min_volume_size(self):
        """Deprecated.  Use default_volume_type_min_size instead"""
        warn(
            "This config property is deprecated. Please use the config "
            "property 'default_volume_type_min_size' or the much more flexible"
            " 'volume_type_properties' instead.")

        return int(self.get("min_volume_size"))

    @property
    def max_volume_size(self):
        """Deprecated.  Use default_volume_type_max_size instead"""
        warn(
            "This config property is deprecated. Please use the config "
            "property 'default_volume_type_max_size' or the much more flexible"
            " 'volume_type_properties' instead.")

        return int(self.get("max_volume_size"))

# Volume create timeouts
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
        amount of time to create timeouts globally for dialing in good test
        timeouts
        """
        return int(self.get("volume_create_base_timeout", default=1))

# Volume delete timeouts
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

# Clone volume timeouts
    @property
    def volume_clone_min_timeout(self):
        """Minimum time to allow any behavior to wait for a volume to finish
        creating when using another volume as its source.
        """
        return int(self.get("volume_clone_min_timeout"))

    @property
    def volume_clone_max_timeout(self):
        """Maximum time to allow any behavior to wait for a volume to finish
        creating when using another volume as its source.
        """
        return int(self.get("volume_clone_max_timeout"))

    @property
    def volume_clone_wait_per_gigabyte(self):
        """Used by some behaviors to attempt to calculate the time it will
        take for a volume to be created based on it's size when using another
        volume as its source
        """
        return int(self.get("volume_clone_wait_per_gigabyte"))

    @property
    def volume_clone_base_timeout(self):
        """Amount of time added by default to the final calculated volume
        clone timeouts for some behaviors.  Useful for adding a constant
        amount of time to clone timeouts globally for dialing in good test
        timeouts.
        """
        return int(self.get("volume_clone_base_timeout"))

# Copy image to volume timeouts
    @property
    def min_volume_from_image_size(self):
        """Minimum size a volume can be if building from an image.
        Used by some behaviors and tests.  Depending on how the environment
        under test is deployed, this value may be superceded by the
        minimum allowed volume size, and is otherwise dependent on the image
        being used for testing.
        """
        return int(self.get("min_volume_from_image_size"))

    @property
    def copy_image_to_volume_base_timeout(self):
        """Base time to add to any calculated copy-image-to-volume timeouts"""
        return int(self.get("copy_image_to_volume_base_timeout"))

    @property
    def copy_image_to_volume_max_timeout(self):
        """Maximum amount in time to wait for a create-volume-from-image
        request to timeout before raising an error
        """
        return int(self.get("copy_image_to_volume_max_timeout"))

    @property
    def copy_image_to_volume_min_timeout(self):
        """Minimum amount in time to wait for a create-volume-from-image
        request to timeout before raising an error
        """
        return int(self.get("copy_image_to_volume_min_timeout"))

    @property
    def copy_image_to_volume_wait_per_gigabyte(self):
        """Amount of time in seconds to wait per gigabyte of size of the image
        being copied to the volume
        """
        return int(self.get("copy_image_to_volume_wait_per_gigabyte"))

# Snapshot create timeouts
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
        snapshot create timeouts for some behaviors.  Useful for adding a
        constant amount of time to volume snapshot timeouts globally for
        dialing in good test timeouts.
        """
        return int(self.get("snapshot_create_base_timeout", default=0))

    @property
    def snapshot_create_wait_per_gigabyte(self):
        """Used by some behaviors to attempt to calculate the time it will
        take for a snapshot to be created based on the size of the original
        volume
        """
        return int(self.get("snapshot_create_wait_per_gigabyte", default=600))

# Snapshot delete timeouts
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
        amount of time to volume snapshot timeouts globally for dialing in good
        test timeouts.
        """
        return int(self.get("snapshot_delete_base_timeout", default=60))

# Restore snapshot to volume timeouts
    @property
    def snapshot_restore_base_timeout(self):
        """Amount of time added by default to the final calculated volume
        snapshot restore timeouts for some behaviors.  Useful for adding a
        constant amount of time to volume snapshot restore timeouts globally
        for dialing in good test timeouts.
        """
        return int(self.get("snapshot_restore_base_timeout"))

    @property
    def snapshot_restore_min_timeout(self):
        """Minimum time to allow any behavior to wait for a snapshot to finish
        restoring to a new volume.
        """
        return int(self.get("snapshot_restore_min_timeout"))

    @property
    def snapshot_restore_max_timeout(self):
        """Maximum time to allow any behavior to wait for a snapshot to finish
        restoring to a new volume.
        """
        return int(self.get("snapshot_restore_max_timeout"))

    @property
    def snapshot_restore_wait_per_gigabyte(self):
        """Used by some behaviors to attempt to calculate the time it will
        take for a snapshot to be restored based on the size of the original
        volume.
        """
        return int(self.get("snapshot_restore_wait_per_gigabyte"))

# Misc
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
    def image_filter_mode(self):
        return self.get("image_filter_mode", 'inclusion')

    @property
    def flavor_filter(self):
        """Expects Json.  Returns an empty dictionary by default (no filter).
        Dictionary keys should be attributes of the flavor model, and key
        values should be a list of values for that model attribute.
        Used by some tests to decide which flavors to target for a given
        test run.
        """
        return json.loads(self.get('flavor_filter', '{}'))

    @property
    def flavor_filter_mode(self):
        return self.get("flavor_filter_mode", 'inclusion')

    @property
    def volume_type_filter(self):
        """Expects Json.  Returns an empty dictionary by default.
        Dictionary keys should be attributes of the volume type model, and
        key values should be a list of values for that model attribute.
        Used by some tests to decide which images to target for a given
        test run.
        """
        return json.loads(self.get('volume_type_filter', '{}'))

    @property
    def volume_type_filter_mode(self):
        return self.get("volume_type_filter_mode", 'inclusion')

# API configuration
    @property
    def allow_snapshot_restore_to_different_type(self):
        return self.get_boolean(
            "allow_snapshot_restore_to_different_type", False)

    @property
    def primary_bootable_volume(self):
        """Introducing this property to handle VIRT-3099- SKS 11-JUL-2018."""
        return self.get("primary_bootable_volume")
