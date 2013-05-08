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


class ImagesConfig(ConfigSectionInterface):

    SECTION_NAME = 'images'

    @property
    def primary_image(self):
        """Default image to be used when building servers in compute tests"""
        return self.get("primary_image")

    @property
    def secondary_image(self):
        """Alternate image to be used in compute tests"""
        return self.get("secondary_image")

    @property
    def image_status_interval(self):
        """Amount of time to wait between polling the status of an image"""
        return int(self.get("image_status_interval"))

    @property
    def snapshot_timeout(self):
        """Length of time to wait before giving up on reaching a status"""
        return int(self.get("snapshot_timeout"))

    @property
    def can_get_deleted_image(self):
        """
        true: Performing a GET on a deleted image returns the image
        false: Performing a GET on a deleted image returns a 404
        """
        return self.get_boolean("can_get_deleted_image")
