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

from cafe.engine.behaviors import BaseBehavior
from common.tools.datagen import rand_name
from images.common.types import ImageContainerFormat, ImageDiskFormat, \
    ImageVisibility
from cloudcafe.common.resources import ResourcePool


class ImagesV2Behaviors(BaseBehavior):
    """
    @summary: Base Behaviors class for Images V2 API tests
    """

    def __init__(self, images_client, images_config):
        super(ImagesV2Behaviors, self).__init__()
        self.config = images_config
        self.client = images_client
        self.resources = ResourcePool()

    def register_basic_image(self):
        """Register a basic image and return its id."""
        response = self.client.create_image(
            name=rand_name('basic_image_'),
            container_format=ImageContainerFormat.BARE,
            disk_format=ImageDiskFormat.RAW)

        image = response.entity

        self.resources.add(self.client.delete_image, image.id_)

        return image.id_

    def register_private_image(self):
        """Register a private image and return its id."""
        response = self.client.create_image(
            name=rand_name('private_image_'),
            visibility=ImageVisibility.PRIVATE,
            container_format=ImageContainerFormat.BARE,
            disk_format=ImageDiskFormat.RAW)

        image = response.entity

        self.resources.add(self.client.delete_image, image.id_)

        return image.id_

    def get_member_ids(self, image_id):
        """Return the list of ids for all available members for an image."""
        response = self.client.list_members(image_id)

        return [member.member_id for member in response.entity]
